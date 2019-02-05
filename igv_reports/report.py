import os
import sys
import json
import math
from urllib.request import urlopen
from igv_reports import fasta, ideogram, data_uri, variant_table, tracks


def create_report_from_vcf(args):

    vcf = args.variants
    info_columns = args.infoColumns.split(",") if args.infoColumns else None
    table = variant_table.VariantTable(vcf, info_columns)

    table_json = table.to_JSON()

    session_dict = {}

    # loop through variants creating an igv.js session for each one
    for tuple in table.features:

        feature = tuple[0]
        unique_id = tuple[1]

        # Center position in 1-based coordinates
        position = math.floor((feature["start"] + feature["end"]) / 2) + 1

        # Define a genomic region around the feature
        chr = feature["chr"]
        start = math.floor(feature["start"] - int(args.flanking) / 2)
        end = math.ceil(feature["end"] + int(args.flanking) / 2)
        region = {"chr": chr, "start": start, "end": end}

        # Fasta
        data = fasta.get_data(args.fasta, region)
        fa = '>' + chr + ':' + str(start) + '-' + str(end) + '\n' + data
        fasta_uri = data_uri.get_data_uri(fa)
        fastaJson = {
            "fastaURL": fasta_uri,
        }

        # Ideogram
        if(args.ideogram):
            ideo_string = ideogram.get_data(args.ideogram, region)
            ideo_uri = data_uri.get_data_uri(ideo_string)
            fastaJson["cytobandURL"] = ideo_uri


        # Initial locus, +/- 20 bases
        initial_locus = chr + ":" + str(position - 20) + "-" + str(position + 20)
        session_json = {
            "locus": initial_locus,
            "reference": fastaJson,
            "tracks": []
        }

        if (args.tracks):
            trackList = args.tracks.split(',')
            for track in trackList:
                trackObj = tracks.get_track_json_dict(track)
                datauri = data_uri.file_to_data_uri(track, trackObj['format'], region)
                trackObj["url"] = datauri

                if(trackObj["type"] == "alignment"):
                    trackObj["height"] = 500

                session_json["tracks"].append(trackObj)


        # Build the session data URI

        session_string = json.dumps(session_json);

        session_uri = data_uri.get_data_uri(session_string)

        session_dict[str(unique_id)] = session_uri

    session_dict = json.dumps(session_dict)

    template_file = args.template
    if None == template_file:
        template_file = os.path.dirname(sys.modules['igv_reports'].__file__) + '/templates/variant_template.html'

    output_file = args.output

    standalone = args.standalone
    with open(template_file, "r") as f:
        data = f.readlines()

        with open(output_file, "w") as o:

            for i, line in enumerate(data):

                if standalone and line.find("<script") and line.find(".js") > 0:
                    print(inline_script(line, o))

                else:
                    j = line.find('"@TABLE_JSON@"')
                    if j >= 0:
                        line = line.replace('"@TABLE_JSON@"', table_json)

                    j = line.find('"@SESSION_DICTIONARY@"')
                    if j >= 0:
                        line = line.replace('"@SESSION_DICTIONARY@"', session_dict)

                    o.write(line)


def inline_script(line, o):
    #<script type="text/javascript" src="https://igv.org/web/test/dist/igv.min.js"></script>
    s = line.find('src="')
    if s > 0:
        e = line.find('">', s)
        url = line[s+5:e]

        response = urlopen(url)
        js = response.read().decode('utf-8')
        response.close()

        o.write('<script type="text/javascript">\n')
        o.write(js)
        o.write('</script>\n')


