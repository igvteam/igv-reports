import os
import sys
import json
import math
import argparse
import yaml
from urllib.request import urlopen
from igv_reports import datauri, tracks, utils, feature
from igv_reports.varianttable import VariantTable
from igv_reports.bedtable import BedTable
from igv_reports.bedtable import BedpeTable
from igv_reports.bedtable import JunctionBedTable
from igv_reports.generictable import GenericTable
from igv_reports.regions import parse_region
from igv_reports.fasta import FastaReader
from igv_reports.ideogram import IdeogramReader
from igv_reports.genome import get_genome
from igv_reports.tracks import get_track_type, is_format_supported
from igv_reports.stream import resource_exists
from igv_reports.utils import resolve_relative_path
from igv_reports.twobit import TwoBitReader
import requests

'''
Create an html report.  This is the main function for the application.
'''


def create_report(args):
    # Read filter config if provided
    filter_config = None
    if args.tabulator and args.filter_config:
        try:
            with open(args.filter_config, 'r') as f:
                filter_config = yaml.safe_load(f)
        except Exception as e:
            print(f"Error reading filter config: {e}")

    # Read the variant data -- this populates the variant table and defines the corresponding regions

    variants_file = args.sites

    if variants_file.endswith(".bcf") or variants_file.endswith(".vcf") or variants_file.endswith(".vcf.gz"):
        table = VariantTable(variants_file, args)

    elif variants_file.endswith(".bed") or variants_file.endswith(".bed.gz"):
        if args.type is not None and args.type == "junction":
            table = JunctionBedTable(variants_file, args.info_columns)
        else:
            table = BedTable(variants_file)

    elif variants_file.endswith(".bedpe") or variants_file.endswith(".bedpe.gz"):
        table = BedpeTable(variants_file)

    elif variants_file.endswith(".maf") or variants_file.endswith(".maf.gz") or (
            args.sequence is not None and args.begin is not None and args.end is not None):
        table = GenericTable.from_tabfile(variants_file, args.info_columns, args.sequence, args.begin, args.end,
                                          args.zero_based)

    elif variants_file.endswith(".json"):
        table = GenericTable.from_fusionjson(variants_file)

    # Track json array.  Tracks can come from (1) --tracks argument, (2) --genome  argument, and (3) --track_config argument
    trackjson = []

    # Check for optional genome argument.
    if args.genome is not None:
        genome = get_genome(args.genome)

        # Sequence - prefer twobit if defined
        if args.twobit is None and "twoBitURL" in genome:
            args.twobit = genome["twoBitURL"]
        elif args.fasta is None and "fastaURL" in genome:
            args.fasta = genome["fastaURL"]

        # Ideogram
        if args.ideogram is None and "cytobandURL" in genome:
            args.ideogram = genome["cytobandURL"]

        # Tracks
        if "tracks" in genome:
            for config in genome["tracks"]:
                if "format" not in config and "url in c":
                    config["format"] = feature.infer_format(config["url"])
                if is_format_supported(config["format"]):
                    if "type" not in config:
                        config["type"] = get_track_type(config["format"])
                    trackjson.append(config)
                else:
                    print("File format: " + config["format"] + " is not supported. Skipping track '" + config[
                        "name"] + "'.")

    # --tracks argument
    if args.tracks is not None:
        for track in args.tracks:
            config = tracks.get_track_json_dict(track)
            # If this is a no-embed report add index URLs
            if args.no_embed == True:
                add_index(config)
            trackjson.append(config)

    # --roi argument
    if args.roi is not None:
        for track in args.roi:
            config = tracks.get_track_json_dict(track)
            config["type"] = "roi"
            # If this is a no-embed report add index URLs
            if args.no_embed == True:
                add_index(config)
            trackjson.append(config)

    # --track_config argument
    if args.track_config is not None:
        for trackobj in args.track_config:
            with open(trackobj) as f:
                j = json.load(f)
                for config in j:
                    if "url" in config:
                        config["url"] = resolve_relative_path(trackobj, config["url"])
                    if "format" not in config and "url" in config:
                        config["format"] = feature.infer_format(config["url"])
                    if "type" not in config:
                        config["type"] = get_track_type(config["format"])
                    trackjson.append(config)

    if args.no_embed == True:
        igv_config = json.dumps(create_noembed_session(args, trackjson))
        locus_dict = json.dumps(create_locus_dict(table, args.window))

    # Create the session dictionary json, containing a session object for each variant
    else:
        session_dict = json.dumps(create_session_dict(args, table, trackjson, args.sampleinfo))

    # Generate the HTML
    template_file = args.template
    if None == template_file:
        if args.type == "junction":
            template_file = os.path.dirname(sys.modules['igv_reports'].__file__) + '/templates/junction_template.html'
        elif args.type == "fusion":
            template_file = os.path.dirname(sys.modules['igv_reports'].__file__) + '/templates/fusion_template.html'
        elif args.no_embed:
            template_file = os.path.dirname(
                sys.modules['igv_reports'].__file__) + '/templates/variant_template-noembed.html'
        elif args.tabulator:
            template_file = os.path.dirname(
                sys.modules['igv_reports'].__file__) + '/templates/variant_template_tabulator.html'
        else:
            template_file = os.path.dirname(sys.modules['igv_reports'].__file__) + '/templates/variant_template.html'

    output_file = args.output

    standalone = args.standalone
    with open(template_file, "r") as f:
        data = f.readlines()

        with open(output_file, "w") as o:

            for i, line in enumerate(data):

                if standalone:
                    if line.strip().startswith("<script") and ".js\"" in line:
                        inline_script(line, o, "js")
                        continue
                    elif line.strip().startswith("<link") and line.strip().endswith("css\">"):
                        inline_script(line, o, "css")
                        continue

                if args.title and line.strip().startswith("<title>"):
                    line = "<title>" + args.title + "</title>"

                if args.header and line.strip().startswith("<!--header-->"):
                    line = "<div>" + read_contents(args.header) + "</div>"

                if args.footer and line.strip().startswith("<!--footer-->"):
                    line = "<div>" + read_contents(args.footer) + "</div>"

                j = line.find('"@TABLE_JSON@"')
                if j >= 0:
                    line = line.replace('"@TABLE_JSON@"', table.to_JSON())

                j = line.find('"@SESSION_DICTIONARY@"')
                if j >= 0:
                    line = line.replace('"@SESSION_DICTIONARY@"', session_dict)

                j = line.find('"@FILTER_CONFIG@"')
                if j >= 0:
                    filter_config_json = json.dumps(filter_config) if filter_config else "null"
                    line = line.replace('"@FILTER_CONFIG@"', filter_config_json)

                j = line.find('"@LOCUS_DICTIONARY@"')
                if j >= 0:
                    line = line.replace('"@LOCUS_DICTIONARY@"', locus_dict)

                j = line.find('"@IGV_CONFIG@"')
                if j >= 0:
                    line = line.replace('"@IGV_CONFIG@"', igv_config)

                sort_option = args.sort.upper() if args.sort is not None else "BASE"
                j = line.find('"@SORT@"')
                if j >= 0:
                    line = line.replace('"@SORT@"', '"' + sort_option + '"')

                o.write(line)


def create_session_dict(args, table, trackjson, sampleinfo):
    ''' Create a dictionary of igv.js session objects, one for each variant '''

    session_dict = {}

    # Create file readers for tracks.  This is done outside the locus loop so initialization happens once
    readers = []
    for config in trackjson:
        readers.append(utils.getreader(config, None, args))

    # Other readers
    if args.fasta is not None:
        sequence_reader = FastaReader(args.fasta)
    elif args.twobit is not None:
        sequence_reader = TwoBitReader(args.twobit)
    else:
        raise ValueError('Must specify either fasta or twobit')

    if args.ideogram is not None:
        ideogram_reader = IdeogramReader(args.ideogram)
    else:
        ideogram_reader = None

    # loop through regions defined from variant, annotation, or bedpe files,  creating an igv.js session for each one
    flanking = 0
    if args.flanking is not None:
        flanking = float(args.flanking)
    i = 0
    for tuple in table.features:
        i += 1
        print(f"Working on variant {i}/{len(table.features)}")

        feature = tuple[0]
        unique_id = tuple[1]

        # If a variant feature (=> row in the table) has an explicit session id use it, otherwise use the row id (i.e. unique_id)
        if hasattr(feature, "session_id"):
            session_id = feature.session_id
        else:
            session_id = str(unique_id)

        if session_id not in session_dict:

            # Placeholder variable for possible second region (bedpe files)
            region2 = None

            # Define a genomic region around the variant
            if hasattr(feature, "viewport"):
                region = parse_region(feature.viewport)
                chr = region["chr"]
                start = region["start"]
                end = region["end"]
            else:
                chr = feature.chr

                if feature.start is not None:
                    start = int(math.floor(feature.start - flanking / 2))
                    start = max(start, 1)  # bound start to 1
                else:
                    start = None
                end = int(math.ceil(feature.end + flanking / 2)) if feature.end is not None else None

                region = {"chr": chr, "start": start, "end": end}

                # If feature has a second locus (bedpe file) create the region here.
                if hasattr(feature, 'chr2') and feature.chr2 is not None:
                    chr2 = feature.chr2
                    start2 = int(math.floor(feature.start2 - flanking / 2))
                    start2 = max(start2, 1)  # bound start to 1
                    end2 = int(math.ceil(feature.end2 + flanking / 2))
                    region2 = {"chr": chr2, "start": start2, "end": end2}

            # Sequence
            data = sequence_reader.slice(region)
            length = sequence_reader.get_reference_length(chr)
            fa = '>' + chr + ':' + str(start) + '-' + str(end) + ' @len=' + str(length) + '\n' + data

            if region2 is not None:
                data2 = sequence_reader.slice(region2)
                length2 = sequence_reader.get_reference_length(chr2)
                fa += '\n' + '>' + chr2 + ':' + str(start2) + '-' + str(end2) + ' @len=' + str(length2) + '\n' + data2

            fasta_uri = datauri.get_data_uri(fa)
            fastaJson = {
                "fastaURL": fasta_uri,
            }

            # Ideogram
            if args.ideogram is not None:
                ideo_string = ideogram_reader.get_data(region["chr"])
                if region2 is not None:
                    ideo_string += ideogram_reader.get_data(region2["chr"])
                ideo_uri = datauri.get_data_uri(ideo_string)
                fastaJson["cytobandURL"] = ideo_uri

            # Initial locus
            if (hasattr(feature, "viewport")):
                initial_locus = feature.viewport
            else:
                initial_locus = locus_string(feature.chr, feature.start, feature.end, args.window)
                if region2 is not None:
                    initial_locus += f' {locus_string(feature.chr2, feature.start2, feature.end2, args.window)}'

            # Loop through track configs
            tracks = []
            if args.translate_sequence_track:
                tracks.append({"type": "sequence", "frameTranslate": True})
            roi = []
            track_order = 1
            idx = 0
            for config in trackjson:

                reader = readers[idx]
                idx += 1

                # "cram" input format is converted to "bam" for output track configs
                if config["format"] == "cram":
                    config["format"] = "bam"

                if config["format"] == "bcf":
                    config["format"] = "vcf"

                # Indexes are not used with data URIs
                if "indexURL" in config:
                    del config["indexURL"]

                data = reader.slice(region, region2)

                # replace url with data URI
                config["url"] = datauri.get_data_uri(data)

                if (config["type"] == "alignment"):
                    if "height" not in config:
                        config["height"] = 500

                    is_snv = feature.end is not None and feature.end - feature.start == 1

                    if (config["type"]) == "alignment" and (args.sort is not None or is_snv) and (
                            args.sort != 'NONE'):
                        sort_option = 'BASE' if args.sort is None else args.sort.upper()
                        config["sort"] = {
                            "option": sort_option,
                            "chr": chr,
                            "position": str(feature.start + 1),
                            "direction": "ASC"
                        }
                if "order" not in config:
                    config["order"] = track_order
                track_order += 1

                if "roi" == config["type"]:
                    roi.append(config)
                else:
                    tracks.append(config)

            session_json = {
                "locus": initial_locus,
                "reference": fastaJson,
                "tracks": tracks
            }
            if len(roi) > 0:
                session_json["roi"] = roi

            # --sampleinfo argument
            if args.sampleinfo is not None:
                sampleinfoJson = []
                for si in args.sampleinfo:
                    data = utils.get_content_as_utf8(si)
                    sampleinfoJson.append({"url": datauri.get_data_uri(data)})
                session_json["sampleinfo"] = sampleinfoJson

            # Build the session data URI
            session_string = json.dumps(session_json)
            session_uri = datauri.get_data_uri(session_string)
            session_dict[session_id] = session_uri

    return session_dict


# Create an igv session config object.  This is used for no-embed reports
def create_noembed_session(args, trackjson):
    if args.fasta is not None:
        reference = {
            "fastaURL": args.fasta
        }
        if resource_exists(args.fasta + ".fai"):
            reference["indexURL"] = args.fasta + ".fai"

    elif args.twobit is not None:
        reference = {
            "twoBitURL": args.twobit
        }
    else:
        raise ValueError('Must specify either fasta or twobit')

    if args.ideogram is not None:
        reference["cytobandURL"] = args.ideogram

    tracks = []
    roi = []
    for tj in trackjson:
        if "roi" == tj["type"]:
            roi.append(tj)
        else:
            tracks.append(tj)
    session = {
        "reference": reference,
        "tracks": tracks
    }
    if len(roi) > 0:
        session["roi"] = roi

    if args.sampleinfo is not None:
        sampleinfoJson = []
        for si in args.sampleinfo:
            sampleinfoJson.append({"url": si})
        session["sampleinfo"] = sampleinfoJson

    return session


def create_locus_dict(table, window):
    locus_dict = {}

    # loop through regions defined from variant, annotation, or bedpe files,  creating  locus for each one

    for tuple in table.features:

        feature = tuple[0]
        unique_id = tuple[1]

        if hasattr(feature, "session_id"):
            session_id = feature.session_id
        else:
            session_id = str(unique_id)

        if (hasattr(feature, "viewport")):
            locus = feature.viewport
        else:
            locus = locus_string(feature.chr, feature.start + 1, feature.end, window)
            if hasattr(feature, 'chr2') and feature.chr2 is not None:
                locus += f' {locus_string(feature.chr2, feature.start2, feature.end2, window)}'

        locus_dict[session_id] = locus

    return locus_dict


def inline_script(line, o, source_type):
    # <script type="text/javascript" src="https://igv.org/web/test/dist/igv.min.js"></script>
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
        url = line[s + offset:e]
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


def locus_string(chr, start, end, window):
    if start is None:
        return chr

    if window is not None:
        window = int(window)
        return f'{chr}:{start + 1 - window / 2}-{end + window / 2}'
    else:
        if (end - start) == 1:
            return f'{chr}:{start + 1}'
        else:
            return f'{chr}:{start + 1}-{end}'


# Potentially add an index URL to a track config.  The "format" field must be set before calling this function
def add_index(config):
    if "url" not in config or "indexURL" in config:
        return

    indexURL = None
    url = config["url"]

    # Check tabix first
    if url.endswith(".gz"):
        if resource_exists(url + ".tbi"):
            indexURL = url + ".tbi"
        elif resource_exists(url + ".csi"):
            indexURL = url + ".csi"

    # Check potential bam/cram files
    if "format" in config:
        format = config["format"]
        if format == "bam":
            if resource_exists(url + ".bai"):
                indexURL = url + ".bai"
            elif resource_exists(format + ".csi"):
                indexURL = url + ".csi"
            else:
                k = url.rfind(".")
                tmp = url[:k] + ".bai"
                if resource_exists(tmp):
                    indexURL = tmp
        elif format == "cram" and indexURL == None:
            if (resource_exists(url + ".crai")):
                indexURL = url + ".crai"

    if indexURL is not None:
        config["indexURL"] = indexURL


def read_contents(file_path):
    """Reads the contents of a file and returns it as a string."""
    if not os.path.exists(file_path):
        raise FileNotFoundError("File not found: " + file_path)
    with open(file_path, 'r') as file:
        return file.read()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sites", help="vcf file defining variants, required")
    parser.add_argument("fasta_", nargs="?", default=None,
                        help="reference fasta file.  Deprecated positional argument,  use --fasta")
    parser.add_argument("--fasta", nargs="?", default=None,
                        help="reference fasta file. One of either --fasta, --twobit, or --genome is required.")
    parser.add_argument("--twobit", nargs="?", default=None,
                        help="reference twobit file. One of either --fasta, --twobit, or --genome is required.")
    parser.add_argument("--genome", help="igv.js genome id (e.g. hg38)")

    parser.add_argument("--type",
                        help="Report type.  Possible values are mutation, junction, and fusion.  Default is mutation")
    parser.add_argument("--ideogram", help="ideogram file in UCSC cytoIdeo format")
    parser.add_argument("--tracks", nargs="+", help="list of track files")
    parser.add_argument("--track-config", nargs="+", help="track json file")
    parser.add_argument("--roi", nargs="+", help="list of region-of-interest files")
    parser.add_argument("--sort",
                        help="initial sort option for alignment tracks.   Supported values include  BASE, STRAND, INSERT_SIZE, and MATE_CHR. Default value is BASE for single nucleotide variants, no sorting otherwise.  See the igv.js documentation for more information. ")
    parser.add_argument("--template", help="html template file", default=None)
    parser.add_argument("--output", help="output file name", default="igvjs_viewer.html")
    parser.add_argument("--info-columns", nargs="+", help="list of VCF info field names to include in variant table")
    parser.add_argument("--info-columns-prefixes", nargs="+",
                        help="list of prefixes of VCF info field names to include in variant table")
    parser.add_argument("--sampleinfo", nargs="+", help="list of sample information files")
    parser.add_argument("--samples", nargs="+",
                        help="Space delimited list of sample (i.e. genotypes) names.  Used in conjunction with --sample-columns")
    parser.add_argument("--sample-columns", nargs="+",
                        help="list of VCF sample (genomtype) FORMAT field names to include in variant table")
    parser.add_argument("--flanking", help="genomic region to include either side of variant", default=1000)
    parser.add_argument("--window",
                        help="initial visible window size (genomic region) in bp.  If not supplied igv.js default applies (41 bp).",
                        default=None)
    parser.add_argument("--standalone", help="embed javascript as well as data in output html", action='store_true')
    parser.add_argument("--title", help="optional title string.  Inserted into the html title tag")
    parser.add_argument("--header", help="optional header html string.  Inserted into the document before the variant table")
    parser.add_argument("--footer", help="optional footer html string.  Inserted into the document below the igv.js viewer")
    parser.add_argument("--sequence", help="Column of sequence (chromosome) name.  For tab-delimited sites file.",
                        default=None)
    parser.add_argument("--begin", help="Column of start position.  For tab-delimited sites file.", default=None)
    parser.add_argument("--end", help="column of end position. For tab-delimited sites file.", default=None)
    parser.add_argument("--zero_based",
                        help="Specify that the position in the data file is 0-based (e.g. UCSC files) rather than 1-based.",
                        default=None)
    parser.add_argument("--idlink", type=str, help="url link template for the VCF ID column")
    parser.add_argument("--exclude-flags", type=int,
                        help="Passed to samtools to filter alignments.  For BAM and CRAM files.", default=1536)
    parser.add_argument("--no-embed", help="Do not embed fasta or track data.  This is not common", action="store_true")
    parser.add_argument("--subsample", type=float,
                        help="Subsample bam files, keeping fraction of input alignments as indicated by input value in the range of 0.0 - 1.0")
    parser.add_argument("--maxlen", type=int, default=10000,
                        help="Maximum length of variant for single  view. Variants exceeding this lenght will be presented in split-screen (multilocus) view")
    parser.add_argument("--translate-sequence-track", help="Three-frame Translate sequence track", action="store_true")
    parser.add_argument("--tabulator", help="Enable Tabulator table with advanced filtering", action="store_true")
    parser.add_argument("--filter-config", help="YAML configuration file for column-specific filtering")

    args = parser.parse_args()

    # For backward compatibility with 'fasta' positional argument
    if args.fasta_ is not None and args.fasta is None:
        args.fasta = args.fasta_
    create_report(args)


if __name__ == "__main__":
    main()
