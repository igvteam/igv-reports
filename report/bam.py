import pysam
import subprocess
from os.path import splitext, basename,join,dirname

from report.regions import merge_regions


def get_bam_data(bam_file, regions=None):
    args = ["-b", "-h",  bam_file]
    if regions:
        args.append(regions)
    return pysam.view(*args)


def get_depth(bam_file, region):

    args = [bam_file, "-r", region]
    depthString = pysam.depth(*args)
    tokens = depthString.split('\n')

    dsum = 0
    count = 0
    for t in tokens:
        t2 = t.split('\t')
        if(len(t) > 2):
            d = int(t2[2])
            count = count + 1
            dsum += d
    if count > 0:
        davg = dsum / count
    else:
        davg = 0

    return davg


# get_sam_data provide primarily for testing
def get_sam_data(bam_file, regions=None):
    args = [bam_file]
    if regions:
        args.extend(regions)
    return pysam.view(*args)











def make_region_bam(bam_file,region):
    bam_region_file=splitext(basename(bam_file))[0]+"."+region+".bam"
    bam_region=join(dirname(bam_file),bam_region_file)
    subprocess.call(["samtools","view","-b",bam_file,region,"-o",bam_region])
    return(bam_region)



