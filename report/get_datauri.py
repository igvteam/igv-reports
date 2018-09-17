from __future__ import print_function

from report import data_uri


def get_datauri(filename, filetype=None, genomic_range=None):
    print(data_uri.file_to_data_uri(filename, filetype, genomic_range))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("filename", help="name of file to be converted to data uri")
    parser.add_argument("-t", "--filetype", help="type of file to be converted to data uri")
    parser.add_argument("-r", "--range" , help="genomic range to be converted - only applicable for bam or tbi files")

    args = parser.parse_args()

    get_datauri(args.filename, filetype=args.filetype, genomic_range=args.range)
