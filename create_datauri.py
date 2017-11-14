import sys
from gzip import compress
from base64 import b64encode

OUTPUT_NAME = "datauri_report.txt"


def file_to_datauri(file_type, filename):
    try:
        with open(filename, 'rb') as input_file, open(OUTPUT_NAME, 'w') as output_file:
            data = input_file.read()
            if not file_type.lower == 'bam':
                data = compress(data)
            enc_str = b64encode(data)
            output_file.write("data:application/gzip;base64," + str(enc_str)[2:-1])

    except OSError as e:
        print(e)


if __name__ == '__main__':
    file_to_datauri(*sys.argv[1:])
