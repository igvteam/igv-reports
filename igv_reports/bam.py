import pysam

def get_data(bam_file, regions=None):
    args = ["-b", "-h",  bam_file]
    if regions:
        args.append(regions)
    return pysam.view(*args)
