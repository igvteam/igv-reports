import sys
from base64 import b64encode
from gzip import compress

from report import bam, tabix, json, fasta


def file_to_data_uri(filename, filetype=None, genomic_range=None):
    if not filetype:
        filetype = infer_filetype(filename)
    else:
        filetype = filetype.lower()

    data = get_data(filename, filetype, genomic_range)
    if filetype != "bam" and filetype != "tbi" and filetype != "gz" and filetype != "json": #and filetype != "bed" and filetype != "fa":
        data = compress(data)
    enc_str = b64encode(data)
    data_uri = "data:application/gzip;base64," + str(enc_str)[2:-1]
    return data_uri


def get_data(filename, filetype, genomic_range):

    if filetype == "bam":
        return bam.get_bam_data(filename, genomic_range)


    if filetype == "json":
        return json.get_data(filename)
    '''
    if filetype == "bed":
        return tabix.get_data(filename, genomic_range)
    if filetype == "fa":
        return fasta.get_data(filename, genomic_range)
    '''

    try:
        with open(filename, "rb") as f:
            return f.read()
    except FileNotFoundError as e:
        print(e, file=sys.stderr)


def infer_filetype(filename):
    filename = filename.lower()
    if filename.endswith(".bam"):
        return "bam"
    elif filename.endswith(".gz.tbi"):
        return "tbi"
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

def create_data_var(data_uris, space=''):
    data = []
    for i, (key, value) in enumerate(data_uris.items()):
        data.append('{}"{}": "{}"{}\n'.format(space + ' ' * 4, key, value, ',' if i < len(data_uris) - 1 else ''))
    return [space + "var data = {\n"] + data + [space+"};\n"]
