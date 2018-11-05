from pyfaidx import Fasta
from os.path import splitext,basename,join,dirname
import unicodedata


def get_data(fasta_file,region=None):

    if None == region:

        with open(fasta_file,"r") as f:

            return(f.read())

    else :

        fasta = Fasta(fasta_file)

        chr_name = region.split(":")[0]
        start = int(((region.split(":")[1])).split("-")[0]) - 1
        end = int(((region.split(":")[1])).split("-")[1])

        slice = fasta[chr_name][start:end]
        slice_name = slice.name
        slice_seq = slice.seq

        return slice_seq

        # extracted_seq=unicodedata.normalize('NFKD',seq_uni).encode('ascii','ignore')
        # prefix = dirname(fasta_file)
        # extracted_region_file = join(prefix, splitext(basename(fasta_file))[0] + genome_range + ".fa")
        # str_ex = str(slice_seq)
        #
        # with open(extracted_region_file, "w") as erf:
        #     erf.write(">" + slice_name + "\n" + str_ex)
        # return (extracted_region_file)