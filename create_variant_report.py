


import os
import sys

from report import data_uri

TEMPLATE_URL = "example/FI_viewer/template.html"
SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))
OUTPUT_FILENAME = "example/FI_viewer/report.html"


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
    config_data.append("{}fastaURL: data[\"{}\"],\n".format(inner_space,fasta_url))
    config_data.append(inner_space + "tracks: [\n")
    for i, name in enumerate(filenames):
        config_data.append(inner_space + " " * 4 + "{\n")
        config_data.append(inner_space + " " * 8 + "url: data[\"" + name + "\"]\n")
        config_data.append("%s}%s\n" % (inner_space + " " * 4, "," if i != len(filenames)-1 else ''))
    config_data.append(inner_space + "]\n")
    return config_data


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("fasta_url", help="fasta file for igv")
    parser.add_argument("filenames", help="comma-delimited list of files to be shown")
    parser.add_argument("-r", "--range" , help="genomic range to be converted - only applicable for bam or tbi files")

    args = parser.parse_args()

    generate_report(args.fasta_url, args.filenames, genomic_region=args.range)



