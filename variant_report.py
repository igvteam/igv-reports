import os
import json
from report import fasta
from report.variant_table import VariantTable
from report import data_uri
from report.vcf import extract_vcf_region
from report.bam import get_bam_data
import report.ideogram


def create_report_from_vcf():
    # TODO -- make all this input
    input = {
        'template': 'example/variants/variant_template.html',
        'output': 'example/variants/igvjs_viewer.html',
        'flanking': 100,
        'panning': 500,
        'vcf': "example/variants/cancer.vcf.gz",
        'info_columns': 'example/variants/info_columns.txt',
        'fasta': '/Users/jrobinso/Dropbox/Data/IGV/hg38.fa',
        'bam': 'example/variants/recalibrated.bam',
        'bed': 'example/variants/refgene.sort.bed.gz',
        'ideogram': 'example/variants/cytoBandIdeo.txt'
    }
    vcf = input['vcf']
    info_columns = input['info_columns']
    table = VariantTable(vcf, info_columns)

    # TODO insert table.toJSON into html file
    table_json = table.to_JSON()
    print(table_json)


    session_dict = {}
    # loop through variants
    for tuple in table.variants:

        variant = tuple[0]
        unique_id = tuple[1]

        chr = variant.chrom
        position = variant.pos - 1
        start = position - input["panning"] / 2
        end = position + input["panning"] / 2

        region = {
            "chr": chr,
            "start": start,
            "end": end
        }

        # Initial locus, +/- 100 bases
        initial_locus =  chr + ":" + str(position - input['flanking']/2) + "-" + str(position + input['flanking']/2)

        #Ideogram
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
        session_json = {
            "locus": initial_locus,
            "reference": fastaJson,
            "tracks": []
        }

        # VCF
        vcfFileString = extract_vcf_region(input['vcf'], chr, start, end)
        vcfData = data_uri.get_data_uri(vcfFileString)
        session_json["tracks"].append({
            "type": "variant",
            "format": "vcf",
            "url": vcfData
        })

        # BAM

        bam_data_uri = data_uri.file_to_data_uri(input['bam'], 'bam', genomic_range = chr + ":" + str(start) + "-" + str(end));
        session_json["tracks"].append( {
            "name": "alignments",
            "type": "alignment",
            "format": "bam",
            "url": bam_data_uri
        })

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

                j = line.find('@TABLE_JSON@')
                if j >= 0:
                    line = line.replace('@TABLE_JSON@', table_json)

                j = line.find('@SESSION_DICTIONARY@')
                if j >= 0:
                    line = line.replace('@SESSION_DICTIONARY@', session_dict)

                o.write(line)


















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