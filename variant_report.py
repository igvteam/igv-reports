import os
import json
from report import data_uri
from report import fasta
from report.variant_table import VariantTable
from report import data_uri


def create_report_from_vcf():
    # TODO -- make all this input
    input = {
        'flanking': 500,
        'vcf': "example/variants/cancer.vcf.gz",
        'info_columns': 'example/variants/info_columns.txt',
        'fasta': '/Users/jrobinso/Dropbox/Data/IGV/hg38.fa'

    }
    vcf = input['vcf']
    info_columns = input['info_columns']
    table = VariantTable(vcf, info_columns)

    # TODO insert table.toJSON into html file

    variants = table.variants;

    # loop through variants
    for variant in table.variants:
        chr = variant.chrom
        position = variant.pos
        start = max(0, position - input["flanking"] - 1)
        end = position + input["flanking"]

        region = {
            "chr": chr,
            "start": start,
            "end": end
        }

        # TODO slice fasta, create reference json

        data = fasta.get_data(input['fasta'], region)
        fa = '>' + chr + ' @start=' + str(start) + '\n' + data
        fasta_uri = data_uri.get_data_uri(fa)
        fastaJson = {
            "fastaURL": fasta_uri
        }
        print(json.dumps(fastaJson))

        # TODO loop through tracks / files,  create track json

        # TODO compress session json, insert into html file var->session table

    # TODO insert var->session table into html file

    # TODO insert javascript functions into html file


# Deprecated methods

TEMPLATE_URL = "example/variants/template.html"
SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))
OUTPUT_FILENAME = "example/variants/report.html"


def createMutationReport(fasta_url, filenames, genomic_region=None):
    with open(TEMPLATE_URL, "r") as f:
        data = f.readlines()

    for i, line in enumerate(data):
        j = line.find('<!-- start igv report here -->')
        if j >= 0:
            space = ' ' * j
            report_start = i + 1
            break
    else:
        return

    filenames = filenames.split(',')
    data_uris = {}
    data_uris[fasta_url] = data_uri.file_to_data_uri(fasta_url)
    for filename in filenames:
        data_uris[filename] = data_uri.file_to_data_uri(filename, genomic_region)

    data_var = data_uri.create_data_var(data_uris, space=space)

    for i in range(report_start, len(data)):
        j = data[i].find("options = {")
        if j >= 0:
            space = ' ' * j
            config_start = i + 1
            break
    else:
        return

    config_data = create_config_data(filenames, space, fasta_url)
    new_html_data = data[:report_start] + data_var + data[report_start:config_start] + config_data + data[config_start:]
    with open(OUTPUT_FILENAME, 'w') as f:
        f.writelines(new_html_data)


def create_config_data(filenames, space, fasta_url):
    inner_space = space + " " * 4
    config_data = []
    config_data.append("{}fastaURL: data[\"{}\"],\n".format(inner_space, fasta_url))
    config_data.append(inner_space + "tracks: [\n")
    for i, name in enumerate(filenames):
        config_data.append(inner_space + " " * 4 + "{\n")
        config_data.append(inner_space + " " * 8 + "url: data[\"" + name + "\"]\n")
        config_data.append("%s}%s\n" % (inner_space + " " * 4, "," if i != len(filenames) - 1 else ''))
    config_data.append(inner_space + "]\n")
    return config_data



if __name__ == "__main__":

    # import argparse
    #
    # parser = argparse.ArgumentParser()
    #
    # parser.add_argument("fasta_url", help="fasta file for igv")
    # parser.add_argument("filenames", help="comma-delimited list of files to be shown")
    # parser.add_argument("-r", "--range", help="genomic range to be converted - only applicable for bam or tbi files")
    #
    # args = parser.parse_args()

    create_report_from_vcf()