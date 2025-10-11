import os

import pysam
import tempfile
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

    # sam flag supports unit tests
    def slice(self, region=None, region2=None, sam = False):

        samargs = ["-h", self.filename]

        if self.args is not None and self.args.subsample is not None:
            samargs.append("--subsample")
            samargs.append(str(self.args.subsample))

        if self.filtetype == "cram" and self.args is not None:
            if self.args.fasta is None:
                raise ValueError("Cram file requires a reference fasta file")
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
            if region['start'] is not None:
                range_string = self.get_chrname(region['chr']) + ":" + str(region['start']) + "-" + str(region['end'])
            else:
                range_string = self.get_chrname(region['chr'])
            samargs.append(range_string)
        if region2:
            range_string = self.get_chrname(region2['chr']) + ":" + str(region2['start']) + "-" + str(region2['end'])
            samargs.append(range_string)

        sam_string = pysam.view(*samargs)

        # Rewrite sam header removing all unnecessary lines
        lines = sam_string.split('\n')
        newlines = []
        for line in lines:
            if line.startswith('@HD') or line.startswith('@RG'):
                newlines.append(line)
            elif line.startswith('@SQ'):
                idx1 = line.find("SN:")
                if idx1 > 0:
                    idx2 = line.find("\t", idx1)
                    sn = line[idx1+3:idx2]
                    if (region and sn == self.get_chrname(region['chr'])) or \
                       (region2 and sn == self.get_chrname(region2['chr'])):
                        newlines.append(line)
            elif not line.startswith('@'):
                newlines.append(line)

        sam_string = '\n'.join(newlines)

        if sam:
            return sam_string

        # convert to bam bytes
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.sam', delete=False) as sam_file:
            sam_file.write(sam_string)
            sam_file.flush()
            sam_filename = sam_file.name
        try:
            bam_bytes = pysam.view('-b', sam_filename, catch_stdout=True)
        finally:
            os.remove(sam_filename)
        return bam_bytes



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
