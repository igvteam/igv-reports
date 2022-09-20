import pysam
from igv_reports.chralias import build_aliastable

class BamReader:

    def __init__(self, filetype, filename, args = None):
        self.filtetype = filetype
        self.filename = filename
        self.args = args

        samargs = ["-H", filename]
        header = pysam.view(*samargs)
        seqnames = parse_seqnames(header)
        self.aliastable = build_aliastable(seqnames)

    # add sam flag for unit tests
    def slice(self, region=None, region2=None,  sam=False):
        if sam:
            samargs = ["-h", self.filename]
        else:
            samargs = ["-b", "-h", self.filename]
        if self.filtetype == "cram" and self.args is not None:
            samargs.append("-T")
            samargs.append(self.args.fasta)

        if self.args is not None and hasattr(self.args, "exclude_flags"):
            if self.args.exclude_flags != 0:
                samargs.append("-F")
                samargs.append(str(self.args.exclude_flags))
        else:
            samargs.append("-F")
            samargs.append("1536")

        if region:
            range_string = self.get_chrname(region['chr']) + ":" + str(region['start']) + "-" + str(region['end'])
            samargs.append(range_string)
        if region2:
            range_string = self.get_chrname(region2['chr']) + ":" + str(region2['start']) + "-" + str(region2['end'])
            samargs.append(range_string)

        return pysam.view(*samargs)

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
