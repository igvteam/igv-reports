from . import regions
from pysam import FastaFile

def get_data(fasta_file,region=None):

    if None == region:

        with open(fasta_file,"r") as f:

            return(f.read())

    else :

        #fasta = Fasta(fasta_file)
        if isinstance(region,str):
            region = regions.parse_region(region)

        chr = region["chr"]
        start = region["start"] - 1
        end = region["end"]

        fasta = FastaFile(fasta_file)

        slice_seq = fasta.fetch(chr , start, end)

        fasta.close()

        return slice_seq

        # extracted_seq=unicodedata.normalize('NFKD',seq_uni).encode('ascii','ignore')
        # prefix = dirname(fasta_file)
        # extracted_region_file = join(prefix, splitext(basename(fasta_file))[0] + genome_range + ".fa")
        # str_ex = str(slice_seq)
        #
        # with open(extracted_region_file, "w") as erf:
        #     erf.write(">" + slice_name + "\n" + str_ex)
        # return (extracted_region_file)