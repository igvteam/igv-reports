import os
import sys

from report import data_uri

QUOTES = {"'", '"'}
SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))


def create_report(url):

    if not url.startswith('/'):
        url = os.path.join(SCRIPT_PATH, url)
    basedir = os.path.dirname(url)
    data_uris = {}
    with open(url, "r") as f:
        data = f.readlines()

    for i, line in enumerate(data):
        j = line.find('<!-- start igv report here -->')
        if j >= 0:
            space = ' ' * j
            report_start = i + 1
            break
    else:
        print("file must contain the line \"<!-- start igv report here -->\"")
        return

    report_data = data[report_start:]

    for line_index, line in enumerate(report_data):
        i = line.lower().find('url:')

        if i >= 0:
            i += 4
            while line[i] not in QUOTES and i < len(line):
                i += 1
            i += 1
            start = i
            while line[i] not in QUOTES and i < len(line):
                i += 1

            filename = line[start:i]
            report_data[line_index] = line[:start - 1] + 'data["' + filename + '"]' + line[i+1:]
            data_uris[filename] = data_uri.file_to_data_uri(os.path.join(basedir, filename))

    new_html_data = data[:report_start] + data_uri.create_data_var(data_uris, space) + report_data

    output_name = os.path.join(basedir, url[:-5] + '_report' + url[-5:])
    with open(output_name, 'w') as f:
        f.writelines(new_html_data)


if __name__ == "__main__":
    create_report(*sys.argv[1:])
