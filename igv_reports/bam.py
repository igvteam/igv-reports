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

    def __init__(self, filename, fasta):
        self.filename = filename
        self.fasta = fasta

    def slice(self, region=None, reference = None):
        args = ["-b", "-h", self.filename]
        if region:
            range_string = region['chr'] + ":" + str(region['start']) + "-" + str(region['end'])
            args.append(range_string)
        if self.fasta:
            args.append("-T" + self.fasta)
        return pysam.view(*args)
