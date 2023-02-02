from . import feature, bam, vcf, wig

def getreader(config, filetype=None, args = None):

    path = config["url"]

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
        return feature.get_featurereader(path)



