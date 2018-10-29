import pysam
import subprocess
from os.path import splitext, basename,join,dirname

def get_bam_data(bam_file, region=None):
    args = ["-b", bam_file]
    if region:
        args.append(region)
    return pysam.view(*args)

def make_region_bam(bam_file,region):
    bam_region_file=splitext(basename(bam_file))[0]+"."+region+".bam"
    bam_region=join(dirname(bam_file),bam_region_file)
    subprocess.call(["samtools","view","-b",bam_file,region,"-o",bam_region])
    return(bam_region)
