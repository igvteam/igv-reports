import os
import sys
import json
import math
import argparse
from urllib.request import urlopen
from igv_reports import fasta, ideogram, datauri, tracks, feature, bam, vcf, utils
from igv_reports.varianttable import VariantTable
from igv_reports.bedtable import BedTable
from igv_reports.bedtable import JunctionBedTable
from igv_reports.generictable import GenericTable
from igv_reports.regions import parse_region
from igv_reports.feature import MockReader

def create_report(args):

    trackreaders = []

    # Read the variant data
    variants_file = args.sites

    if variants_file.endswith(".bcf") or variants_file.endswith(".vcf") or variants_file.endswith (".vcf.gz"):
        table = VariantTable(variants_file, args.info_columns, args.info_columns_prefixes, args.sample_columns)

    elif variants_file.endswith(".bed") or variants_file.endswith(".bed.gz"):
        if args.type is not None and args.type == "junction":
            table = JunctionBedTable(variants_file, args.info_columns)
        else:
            table = BedTable(variants_file, args.split)

    elif variants_file.endswith(".maf") or variants_file.endswith(".maf.gz") or (args.sequence is not None and args.begin is not None and args.end is not None):
        table = GenericTable(variants_file, args.info_columns, args.sequence, args.begin, args.end, args.zero_based)
        # A hack -- since these file formats are not supported by igv.js mock up a bed style track
        flist = []
        for tuple in table.features:
            flist.append(tuple[0])
        trackreaders.append({
            "track": "variants.bed",
            "reader": MockReader(flist)
        })


    table_json = table.to_JSON()

    session_dict = {}

    # Create file readers for tracks.  This is done outside the loucs loop so initialization happens once

    if args.tracks is not None:
        for track in args.tracks:
            reader = utils.getreader(track, None, args.fasta)
            trackreaders.append({
                "track": track,
                "reader": reader
            })

    trackconfigs = []
    if args.track_config is not None:
        for trackobj in args.track_config:
            with open(trackobj) as f:
                data = json.load(f)
                for config in data:
                    reader = utils.getreader(config["url"])
                    trackconfigs.append({
                        "config": config,
                        "reader": reader
                    })



    # loop through variants creating an igv.js session for each one
    flanking = 0
    if args.flanking is not None:
        flanking = float(args.flanking)

    i = 0
    for tuple in table.features:
        i += 1
        print(f"Working on variant {i}/{len(table.features)}")

        feature = tuple[0]
        unique_id = tuple[1]
        if hasattr(feature, "session_id"):
            session_id = feature.session_id
        else:
            session_id = str(unique_id)

        if session_id not in session_dict:

            # Define a genomic region around the variant
            if hasattr(feature, "viewport"):
                region = parse_region(feature.viewport)
                chr = region["chr"]
                start = region["start"]
                end = region["end"]
            else:
                chr = feature.chr
                start = int (math.floor(feature.start - flanking / 2))
                start = max(start,1) # bound start to 1
                end = int (math.ceil(feature.end + flanking / 2))
                region = {
                    "chr": chr,
                    "start": start,
                    "end": end
                }
                if args.split:
                    chr2 = feature.chr2
                    start2 = int (math.floor(feature.start2 - flanking / 2))
                    start2 = max(start2,1) # bound start to 1
                    end2 = int (math.ceil(feature.end2 + flanking / 2))
                    region2 = {
                        "chr": chr2,
                        "start": start2,
                        "end": end2
                    }

            # Fasta
            data = fasta.get_data(args.fasta, region)
            if not args.split:
                fa = '>' + chr + ':' + str(start) + '-' + str(end) + '\n' + data
            else:
                data2 = fasta.get_data(args.fasta, region2)
                fa = '>' + chr + ':' + str(start) + '-' + str(end) + '\n' + data + '\n' + '>' + chr2 + ':' + str(start2) + '-' + str(end2) + '\n' + data2
            fasta_uri = datauri.get_data_uri(fa)
            fastaJson = {
                "fastaURL": fasta_uri,
            }

            # Ideogram
            if(args.ideogram):
                if not args.split:
                    ideo_string = ideogram.get_data(args.ideogram, region)
                else:
                    ideo_string = ideogram.get_data(args.ideogram, region) + ideogram.get_data(args.ideogram, region2)
                ideo_uri = datauri.get_data_uri(ideo_string)
                fastaJson["cytobandURL"] = ideo_uri


            # Initial locus, +/- 20 bases
            if(hasattr(feature, "viewport")):
                initial_locus = feature.viewport
            else:
                if not args.split:
                    position = int(math.floor((feature.start + feature.end) / 2)) + 1   # center of region in 1-based coordinates
                    initial_locus = chr + ":" + str(position)
                else:
                    position = int(math.floor((feature.start + feature.end) / 2)) + 1   # center of region in 1-based coordinates
                    position2 = int(math.floor((feature.start2 + feature.end2) / 2)) + 1   # center of region in 1-based coordinates
                    initial_locus = chr + ":" + str(position) + " " + chr2 + ":" + str(position2)
            session_json = {
                "locus": initial_locus,
                "reference": fastaJson,
                "tracks": []
            }


            track_objects = []
            for tr in trackreaders:
                track = tr["track"]
                reader = tr["reader"]
                trackobj = tracks.get_track_json_dict(track)
                if not args.split:
                    data = reader.slice(region)
                else:
                    data = reader.slice(region, region2=region2, split_bool=args.split)
                trackobj["url"] = datauri.get_data_uri(data)
                track_objects.append(trackobj)

            # Loop through user supplied track configs
            # "cram" input format is converted to "bam" for output track configs
            for tc in trackconfigs:
                trackobj = tc["config"];
                default_trackobj = tracks.get_track_json_dict(trackobj["url"]);
                if "type"  not in trackobj:
                    trackobj["type"] = default_trackobj["type"]
                if "format" not in trackobj:
                    trackobj["format"] = default_trackobj["format"]
                if trackobj["format"] == "cram":
                    trackobj["format"] = "bam"
                if "name" not in trackobj:
                    trackobj["name"] = default_trackobj["url"]
                if "indexURL" in trackobj:
                    del trackobj["indexURL"]
                reader = tc["reader"]
                data = reader.slice(region)
                trackobj["url"] = datauri.get_data_uri(data)
                track_objects.append(trackobj)

            track_order = 1
            for trackobj in track_objects:
                if(trackobj["type"] == "alignment"):
                    trackobj["height"] = 500
                    is_snv = feature.end - feature.start == 1
                    if (trackobj["type"]) == "alignment" and (args.sort is not None or is_snv) and (args.sort != 'NONE'):
                        sort_option = 'BASE' if args.sort is None else args.sort.upper()
                        trackobj["sort"] = {
                            "option": sort_option,
                            "chr": chr,
                            "position": str(feature.start + 1),
                            "direction": "ASC"
                     }
                if "order" not in trackobj:
                    trackobj["order"] = track_order
                session_json["tracks"].append(trackobj)
                track_order += 1



    # Build the session data URI

            session_string = json.dumps(session_json)
            session_uri = datauri.get_data_uri(session_string)
            session_dict[session_id] = session_uri

    session_dict = json.dumps(session_dict)

    template_file = args.template
    if None == template_file:
        if 'junction' == args.type:
            template_file = os.path.dirname(sys.modules['igv_reports'].__file__) + '/templates/junction_template.html'
        else:
            template_file = os.path.dirname(sys.modules['igv_reports'].__file__) + '/templates/variant_template-2.html'

    output_file = args.output

    standalone = args.standalone
    with open(template_file, "r") as f:
        data = f.readlines()

        with open(output_file, "w") as o:

            for i, line in enumerate(data):

                if args.title is not None and line.startswith("<!--title-->"):
                    o.write("<h1>" + args.title + "</h1>")

                if standalone:
                    if line.strip().startswith("<script") and ".js\"" in line:
                        inline_script(line, o, "js")
                        continue
                    elif line.strip().startswith("<link") and line.strip().endswith("css\">"):
                        inline_script(line, o, "css")
                        continue
                j = line.find('"@TABLE_JSON@"')
                if j >= 0:
                    line = line.replace('"@TABLE_JSON@"', table_json)

                j = line.find('"@SESSION_DICTIONARY@"')
                if j >= 0:
                    line = line.replace('"@SESSION_DICTIONARY@"', session_dict)

                o.write(line)


def inline_script(line, o, source_type):
    #<script type="text/javascript" src="https://igv.org/web/test/dist/igv.min.js"></script>
    if source_type == "js":
        s = line.find('src="')
        offset = 5
        o.write('<script type="text/javascript">\n')
    elif source_type == "css":
        s = line.find('href="')
        offset = 6
        o.write('<style type="text/css">\n')
    else:
        raise KeyError("Inline script must be either js- or css-file")
    if s > 0:
        e = line.find('">', s)
        url = line[s+offset:e]
        response = urlopen(url)
        content = response.read().decode('utf-8')
        response.close()
        o.write(content)
        if source_type == "js":
            o.write('</script>\n')
        else:
            o.write('</style>\n')
    else:
        raise ValueError("No file path in {l} for inline script.".format(l=line))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sites", help="vcf file defining variants, required")
    parser.add_argument("fasta", help="reference fasta file, required")
    parser.add_argument("--type", help="Report type.  Possible values are mutation and junctions.  Default is mutation")
    parser.add_argument("--ideogram", help="ideogram file in UCSC cytoIdeo format")
    parser.add_argument("--tracks", nargs="+", help="list of track files")
    parser.add_argument("--track-config", nargs="+", help="track json file")
    parser.add_argument("--sort", help="initial sort option for alignment tracks.   Supported values include  BASE, STRAND, INSERT_SIZE, and MATE_CHR. Default value is BASE for single nucleotide variants, no sorting otherwise.  See the igv.js documentation for more information. ")
    parser.add_argument("--template", help="html template file", default=None)
    parser.add_argument("--output", help="output file name", default="igvjs_viewer.html")
    parser.add_argument("--info-columns", nargs="+", help="list of VCF info field names to include in variant table")
    parser.add_argument("--info-columns-prefixes", nargs="+", help="list of prefixes of VCF info field names to include in variant table")
    parser.add_argument("--sample-columns", nargs="+", help="list of VCF sample/format field names to include in variant table")
    parser.add_argument("--flanking", help="genomic region to include either side of variant", default=1000)
    parser.add_argument("--standalone", help='Print more data', action='store_true')
    parser.add_argument("--title", help="optional title string")
    parser.add_argument("--sequence", help="Column of sequence (chromosome) name.  For tab-delimited sites file.", default=None)
    parser.add_argument("--begin", help="Column of start position.  For tab-delimited sites file.", default=None)
    parser.add_argument("--end", help="column of end position. For tab-delimited sites file.", default=None)
    parser.add_argument("--zero_based", help="Specify that the position in the data file is 0-based (e.g. UCSC files) rather than 1-based.", default=None)
    parser.add_argument("--split", help="Specify whether multi locus view is needed by the input data.", action="store_true")
    args = parser.parse_args()
    create_report(args)

if __name__ == "__main__":

    main()
