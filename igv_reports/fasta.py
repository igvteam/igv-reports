from . import regions
import pysam

def get_data(fasta_file,region=None):

    if None == region:

        with open(fasta_file,"r") as f:
            return(f.read())

    else :

        if isinstance(region,str):
            region = regions.parse_region(region)

        chr = region["chr"]
        start = region["start"] - 1
        end = region["end"]

        fasta = pysam.FastaFile(fasta_file)

        slice_seq = fasta.fetch(chr, start, end)

        fasta.close()

        return slice_seq

class FastaReader:

    def __init__(self, file):
        self.fasta = pysam.FastaFile(file)

    def slice(self, region = None):

        if None == region:
            with open(self.fasta,"r") as f:
                return(f.read())

        else :

            if isinstance(region,str):
                region = regions.parse_region(region)

            chr = region["chr"]
            start = region["start"] - 1 if region["start"] is not None else None
            end = region["end"] if region["end"] is not None else None

            try:
                seq = self.fasta.fetch(chr, start, end)


            except KeyError:
                chr = "chr" + chr
                seq = self.fasta.fetch(chr, start, end)

            return seq


