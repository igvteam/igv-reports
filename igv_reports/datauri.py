
from base64 import b64encode
from gzip import compress
import argparse
from . import utils
from .regions import parse_region


#This module exports functions to convert text or binary data to a data URI readable by igv.js.

def get_data_uri(data):

    """
    Return a data uri for the input, which can be either a string or byte array
    """

    if isinstance(data, str):
        data = compress(data.encode())
        mediatype = "data:application/gzip"
    else:
        if data[0] == 0x1f and data[1] == 0x8b:
            mediatype = "data:application/gzip"
        else:
            mediatype = "data:application:octet-stream"

    enc_str = b64encode(data)

    data_uri = mediatype + ";base64," + str(enc_str)[2:-1]
    return data_uri


def file_to_data_uri(filename, filetype=None, genomic_range=None):
    reader = utils.getreader(filename, filetype)
    region = parse_region(genomic_range) if genomic_range else None
    data = reader.slice(region)
    data_uri = get_data_uri(data)
    return data_uri


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="name of file to be converted to data uri")
    parser.add_argument("-t", "--filetype", help="type of file to be converted to data uri")
    parser.add_argument("-r", "--region" , help="genomic region to be converted in the form chr:start-stop")
    args = parser.parse_args()

    if args.region:
        region = parse_region(args.region)
    else:
        region = None

    uri = file_to_data_uri(args.filename, args.filetype, region)
    print(uri)

if __name__ == "__main__":
    main()
