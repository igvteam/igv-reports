import pysam


def get_bam_data(bam_file, region=None):
    args = ["-b", bam_file]
    if region:
        args.append(region)
    return pysam.view(*args)
