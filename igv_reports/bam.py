import os
import pysam


def get_data(bam_file, region=None):
    args = ["-b", "-h", bam_file]
    if region:
        range_string = region['chr'] + ":" + str(region['start']) + "-" + str(region['end'])
        args.append(range_string)
    return pysam.view(*args)


# Return data in sam format -- for unit tests
def get_sam_data(bam_file, region=None):
    args = ["-h", bam_file]
    if region:
        range_string = region['chr'] + ":" + str(region['start']) + "-" + str(region['end'])
        args.append(range_string)
    return pysam.view(*args)


class BamReader:

    def __init__(self, filename, fasta=None):
        self.filename = filename
        self.fasta = fasta

    # add sam flag for unit tests
    def slice(self, region=None, reference=None, region2=None, split_bool=False, sam=False):
        if sam:
            args = ["-h", self.filename]
        else:
            args = ["-b", "-h", self.filename]
        if self.fasta:
            args.append("-T" + self.fasta)
        if region:
            range_string = region['chr'] + ":" + str(region['start']) + "-" + str(region['end'])
            args.append(range_string)
        if region2:
            range_string = region2['chr'] + ":" + str(region2['start']) + "-" + str(region2['end'])
            args.append(range_string)

        return pysam.view(*args)
