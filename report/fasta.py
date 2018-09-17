from pyfaidx import Fasta
from os.path import splitext,basename,join,dirname
import unicodedata

def extract_fasta_seq(fasta_file,genome_range):
    whole_seq=Fasta(fasta_file)
    chr_name=genome_range.split(":")[0]
    start=((genome_range.split(":")[1])).split("-")[0]
    end=((genome_range.split(":")[1])).split("-")[1]
    one_chr=whole_seq[chr_name]
    one_seq=whole_seq[chr_name][int(start):int(end)]
    extracted_name=one_seq.name
    extracted_seq=one_seq.seq
    #extracted_seq=unicodedata.normalize('NFKD',seq_uni).encode('ascii','ignore')
    prefix=dirname(fasta_file)
    extracted_region_file=join(prefix,splitext(basename(fasta_file))[0]+genome_range+".fa")
    str_ex=str(extracted_seq)
    with open(extracted_region_file,"w") as erf:
        erf.write(">"+extracted_name+"\n"+str_ex)
    return(extracted_region_file)

def get_data(fasta_file,region=None):
    with open(fasta_file,"r") as f:
        return(bytes(f.read(),"utf-8"))
