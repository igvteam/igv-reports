import pysam
from igv_reports.chralias import build_aliastable

class BamReader:

    def __init__(self, filename, fasta=None):
        self.filename = filename
        self.fasta = fasta

        args = ["-H", filename]
        header = pysam.view(*args)
        seqnames = parse_seqnames(header)
        self.aliastable = build_aliastable(seqnames)

    # add sam flag for unit tests
    def slice(self, region=None, region2=None,  sam=False):
        if sam:
            args = ["-h", self.filename]
        else:
            args = ["-b", "-h", self.filename]
        if self.fasta:
            args.append("-T")
            args.append(self.fasta)
        if region:
            range_string = self.get_chrname(region['chr']) + ":" + str(region['start']) + "-" + str(region['end'])
            args.append(range_string)
        if region2:
            range_string = self.get_chrname(region2['chr']) + ":" + str(region2['start']) + "-" + str(region2['end'])
            args.append(range_string)

        return pysam.view(*args)

    def get_chrname(self, c):
        if c in self.aliastable:
            return self.aliastable[c]
        else:
            return c



def parse_seqnames(header):
    seqnames = []
    lines = header.split('\n')
    for line in lines:
        if line.startswith('@SQ'):
            idx1 = line.find("SN:")
            if idx1 > 0:
                idx2 = line.find("\t", idx1)
                seqnames.append(line[idx1+3:idx2])

    return seqnames
