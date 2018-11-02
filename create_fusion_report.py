from __future__ import print_function
import os

from report import data_uri

QUOTES = {"'", '"'}
SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))


def create_fusion_report(template):

    basedir = os.path.dirname(template)
    data_uris = {}

    with open(template, "r") as f:
        data = f.readlines()


    for i, line in enumerate(data):
        j = line.find('<!-- start igv report here -->')
        if j >= 0:
            found = True
            space = ' ' * j
            report_start = i + 1
            break

    else:
        print("file must contain the line \"<!-- start igv report here -->\"")
        return

    input_lines = data[report_start:]
    output_lines = []

    for line_index, line in enumerate(input_lines):

        is_index = line.find('indexURL:') > 0
        if is_index:
            continue

        i = line.lower().find('url:')
        json_line = line.lower().find('getjson(')
        if i >= 0:
            i += 4
            while line[i] not in QUOTES and i < len(line):
                i += 1
            i += 1
            start = i
            while line[i] not in QUOTES and i < len(line):
                i += 1
            filename = line[start:i]
            output_lines.append(line[:start - 1] + 'data["' + filename + '"]' + line[i+1:])
            data_uris[filename] = data_uri.file_to_data_uri(os.path.join(basedir, filename))

        elif json_line >= 0:
            i += 6
            while line[i] not in QUOTES and i < len(line):
                i += 1
            i += 1
            start = i
            while line[i] not in QUOTES and i < len(line):
                i += 1
            filename = line[start:i]
            json_uri=data_uri.file_to_data_uri(os.path.join(basedir, filename))

            output_lines.append(line[:start - 1] + '"'+json_uri+'"'+line[i+1:])

        else:
            output_lines.append(line)

    report_header =  data[:report_start]

    report_data_uris = data_uri.create_data_var(data_uris, space)

    report_body = output_lines

    new_html_data = report_header + report_data_uris + report_body

    output_name = os.path.join(template[:-5] + '_report' + template[-5:])
    with open(output_name, 'w') as f:
        f.writelines(new_html_data)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="the html file to be converted")
    args = parser.parse_args()

    create_fusion_report(args.filename)
