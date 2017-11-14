import os
import sys
from gzip import compress
from base64 import b64encode

QUOTES = {"'", '"'}
SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))


def create_report(url):

    if not url.startswith('/'):
        url = os.path.join(SCRIPT_PATH, url)
    basedir = os.path.dirname(url)
    data_uris = {}
    data = get_data(url, as_array=True)
    report_start = -1
    space = ''

    for i, line in enumerate(data):
        j = line.find('<!-- start igv report here -->')
        if j >= 0:
            space = ' ' * j
            report_start = i + 1
            break

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

            file_data = get_data(os.path.join(basedir, filename), binary=True)

            if not filename.lower().endswith('bam'):  # bam files are already compressed
                file_data = compress(file_data)
            enc_str = b64encode(file_data)
            data_uris[filename] = 'data:application/gzip;base64,' + str(enc_str)[2:-1]

    new_html_data = data[:report_start] + data_list(data_uris, space) + report_data

    output_name = os.path.join(basedir, url[:-5] + '_report' + url[-5:])
    with open(output_name, 'w') as f:
        f.writelines(new_html_data)


def get_data(url, binary=False, as_array=False):
    mode = 'rb' if binary else 'r'
    with open(url, mode) as f:
        return f.readlines() if as_array else f.read()


def data_list(data_uris, space=''):
    data = []
    for i, (key, value) in enumerate(data_uris.items()):
        data.append('{}"{}": "{}"{}\n'.format(space + ' ' * 4, key, value, ',' if i < len(data_uris) - 1 else ''))
    return [space + "var data = {\n"] + data + [space+"};\n"]


if __name__ == "__main__":
    create_report(*sys.argv[1:])
