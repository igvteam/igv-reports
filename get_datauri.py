from __future__ import print_function
import sys

from report import data_uri


def get_datauri(filename, filetype=None, genomic_range=None):
    print(data_uri.file_to_data_uri(filename, filetype, genomic_range))


if __name__ == "__main__":
    if 1 <= len(sys.argv) <= 3:
        get_datauri(*sys.argv)
    else:
        print("Usage: python get_datauri.py [filename] [file-type] [genomic range]")
