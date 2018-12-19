import sys
from base64 import b64encode
from gzip import compress

from report import bam, vcf, tracks, tabix

# application/octet-stream

def get_data_uri(data):

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
        filetype = infer_filetype(filename)
    else:
        filetype = filetype.lower()

    data = get_data(filename, filetype, genomic_range)

    data_uri = get_data_uri(data)

    return data_uri


def get_data(filename, filetype, genomic_range):

    if(genomic_range):
        range_string = genomic_range['chr'] + ":" + str(genomic_range['start']) + "-" + str(genomic_range['end'])
    else:
        range_string = None

    if filetype == "bam":
        return bam.get_data(filename, range_string)

    elif filetype == "vcf":
        return vcf.extract_vcf_region(input['variants'], genomic_range)

    elif tracks.istabix(filename):
        return tabix.get_data(filename, range_string)

    elif filename.endswith(".gz"):
        with open(filename, "rb") as f:
            return f.read()
    else:
        with open(filename,"r") as f:
            b = bytes(f.read(),"utf-8")
            if filetype == 'json':
                return b     # Quirk of jQuery, used in fusion report -- can't handle gzipped data urls
            else:
                return compress(b)



def infer_filetype(filename):
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

def create_data_var(data_uris, space=''):
    data = []
    for i, (key, value) in enumerate(data_uris.items()):
        data.append('{}"{}": "{}"{}\n'.format(space + ' ' * 4, key, value, ',' if i < len(data_uris) - 1 else ''))
    return [space + "var data = {\n"] + data + [space+"};\n"]
