from . import feature, bam, vcf

def getreader(config, filetype=None, fasta=None):

    path = config["url"]

    if not filetype:
        filetype = feature.infer_format(path)
    else:
        filetype = filetype.lower()

    if filetype == "bam" :
        return bam.BamReader(path)

    if filetype == "cram":
        return bam.BamReader(path, fasta)


    elif filetype == "vcf" or filetype == "bcf":
        return vcf.VcfReader(path)

    else:
        return feature.get_featurereader(path)



