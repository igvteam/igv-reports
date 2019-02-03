import os
from base64 import b64encode
from gzip import compress
from . import bam, vcf, tabix


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

    if not filetype:
        filetype = _infer_filetype(filename)
    else:
        filetype = filetype.lower()

    data = _get_data(filename, filetype, genomic_range)

    data_uri = get_data_uri(data)

    return data_uri


def _get_data(filename, filetype, region):

    if filetype == "bam":
        return bam.get_data(filename, region)

    elif filetype == "vcf":
        return vcf.get_data(input['variants'], region)

    elif _istabix(filename):
        return tabix.get_data(filename, region)

    else:

        if region != None:
            raise Exception("Track files must be indexed with tabix.  No index found for: " + filename)

        if filename.endswith(".gz"):
            with open(filename, "rb") as f:
                return f.read()
        else:
            with open(filename,"r") as f:
                return f.read()



def _infer_filetype(filename):
    filename = filename.lower()
    if filename.endswith(".bam"):
        return "bam"
    elif filename.endswith(".fa"):
        return "fa"
    elif filename.endswith(".gz"):
        return "gz"
    elif filename.endswith(".json"):
        return "json"
    '''
    elif filename.endswith(".bed"):
        return "bed"
    '''


def _istabix(filename):

    # If this is a url we will be hopeful that the index is there.  pysam will throw an exception if it is not
    if (filename.startswith("http://") or filename.startswith("https://")) and filename.endswith(".gz"):
        return True
    else:
        return filename.endswith(".gz") and (os.path.exists(filename + ".tbi") or os.path.exists(filename + ".csi"))