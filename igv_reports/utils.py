from os import path
from .stream import getstream
from . import feature, bam, vcf, wig

def getreader(config, filetype=None, args = None):

    path = config["url"]
    indexed = config["indexed"] if "indexed" in config else True    # Assume true until proven otherwise

    if not filetype:
        filetype = feature.infer_format(path)
    else:
        filetype = filetype.lower()

    if filetype == "bam" or filetype == "cram" :
        return bam.BamReader(filetype, path, args)

    elif filetype == "vcf" or filetype == "bcf":
        return vcf.VcfReader(path)
    
    elif filetype == "wig":
        return wig.WigReader(path)

    else:
        return feature.get_featurereader(config)



def resolve_relative_path(path1, path2):

    if path2.startswith("http://") or path2.startswith("https://") or path.isabs(path2):
        return path2

    if path1.startswith("http://") or path1.startswith("https://"):
        qIdx = path1.find("?")
        strippedURL = path1[0:qIdx] if qIdx > 0 else path1
        query = path1[qIdx::] if qIdx > 0 else ""
        lastSlashIdx  = len(strippedURL) - strippedURL[::-1].find("/")
        return strippedURL[0:lastSlashIdx] + path2 + query

    else:
        if path.exists(path2):
            return path2
        else:
            dir = path.dirname(path1)
            return path.join(dir, path2)


def get_content_as_utf8(source):
    """
    Reads the content from a local file or a URL and returns it as a UTF-8 string.

    Args:
        source (str): The local file path or URL.

    Returns:
        str: The content as a UTF-8 string.
    """
    f = getstream(source)
    return f.read()
