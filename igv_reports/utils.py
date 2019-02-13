import io
import gzip
import requests
from . import feature, bam, vcf



def getreader(path, filetype=None):

    if not filetype:
        filetype = feature.infer_format(path)
    else:
        filetype = filetype.lower()

    if filetype == "bam" or filetype == "cram":
        return bam.BamReader(path)

    elif filetype == "vcf":
        return vcf.VcfReader(path)

    else:
        return feature.FeatureReader(path)

