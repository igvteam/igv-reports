import os
import json
import argparse

from report import fasta
from report.variant_table import VariantTable
from report import data_uri
from report.vcf import extract_vcf_region
from report import tracks
import report.ideogram
import report.tabix


def create_report_from_vcf():
    # TODO -- make all this input
    input = {
        'template': 'example/variants/variant_template.html',
        'output': 'example/variants/igvjs_viewer.html',
        'flanking': 1000,
        'variants': "example/variants/cancer.vcf.gz",
        'infoColumns': "GENE,TISSUE,TUMOR,COSMIC_ID,GENE,SOMATIC",
        'fasta': '/Users/jrobinso/Dropbox/Data/IGV/hg38.fa',
        'tracks': 'example/variants/recalibrated.bam,example/variants/refgene.sort.bed.gz',
        'ideogram': 'example/variants/cytoBandIdeo.txt'
    }
    vcf = input['variants']
    info_columns = input['infoColumns']
    table = VariantTable(vcf, info_columns)

    table_json = table.to_JSON()
    print(table_json)

    session_dict = {}
    # loop through variants
    for tuple in table.variants:
        variant = tuple[0]
        unique_id = tuple[1]

        chr = variant.chrom
        position = variant.pos - 1
        start = position - input["flanking"] / 2
        end = position + input["flanking"] / 2

        region = {
            "chr": chr,
            "start": start,
            "end": end
        }

        # Ideogram
        ideo_string = report.ideogram.fetch_chromosome(input['ideogram'], chr)
        ideo_uri = data_uri.get_data_uri(ideo_string)

        # Fasta
        data = fasta.get_data(input['fasta'], region)
        fa = '>' + chr + ':' + str(start) + '-' + str(end) + '\n' + data
        fasta_uri = data_uri.get_data_uri(fa)
        fastaJson = {
            "fastaURL": fasta_uri,
            "cytobandURL": ideo_uri
        }

        # Initial locus, +/- 20 bases
        initial_locus = chr + ":" + str(position - 20) + "-" + str(position + 20)
        session_json = {
            "locus": initial_locus,
            "reference": fastaJson,
            "tracks": []
        }

        if(input['tracks']):
            tracks = input['tracks'].split(',')
            for track in tracks:
                trackObj = report.tracks.get_track_json_dict(track)
                datauri = data_uri.file_to_data_uri(track, trackObj['format'], region)
                trackObj["url"] = datauri
                session_json["tracks"].append(trackObj)


        # Build session uri

        session_string = json.dumps(session_json);

        session_uri = data_uri.get_data_uri(session_string)

        session_dict[str(unique_id)] = session_uri

    session_dict = json.dumps(session_dict)

    template_file = input['template']
    output_file = input['output']

    with open(template_file, "r") as f:
        data = f.readlines()

        with open(output_file, "w") as o:

            for i, line in enumerate(data):

                j = line.find('"@TABLE_JSON@"')
                if j >= 0:
                    line = line.replace('"@TABLE_JSON@"', table_json)

                j = line.find('"@SESSION_DICTIONARY@"')
                if j >= 0:
                    line = line.replace('"@SESSION_DICTIONARY@"', session_dict)

                o.write(line)


if __name__ == "__main__":


    parser = argparse.ArgumentParser()

    parser.add_argument("variants", help="vcf file defining variants, required")
    parser.add_argument("--fasta", help="reference fasta file, required")
    parser.add_argument("--ideogram", help="ideogram file in UCSC cytoIdeo format")
    parser.add_argument("--tracks", help="comma-delimited list of track files")
    parser.add_argument("--template", help="html template file", default="example/variants/variant_template.html")
    parser.add_argument("--infoColumns", help="comma delimited list of info column names for variant table")

    args = parser.parse_args()

    create_report_from_vcf()

    input = {
        'template': 'example/variants/variant_template.html',
        'output': 'example/variants/igvjs_viewer.html',
        'flanking': 500,
        'vcf': "example/variants/cancer.vcf.gz",
        'info_columns': 'example/variants/info_columns.txt',
        'fasta': '/Users/jrobinso/Dropbox/Data/IGV/hg38.fa',
        'bam': 'example/variants/recalibrated.bam',
        'bed': 'example/variants/refgene.sort.bed.gz',
        'ideogram': 'example/variants/cytoBandIdeo.txt'
    }
