from . import feature, bam, vcf

def getreader(path, filetype=None, fasta=None):

    if not filetype:
        filetype = feature.infer_format(path)
    else:
        filetype = filetype.lower()

    if filetype == "bam" :
        return bam.BamReader(path, fasta)

    elif filetype == "cram":
        return bam.BamReader(path, fasta)

    elif filetype == "vcf":
        return vcf.VcfReader(path)

    else:
        return feature.FeatureReader(path)

