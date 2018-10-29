import pysam
from os.path import join,dirname

def get_data(filename, genomic_range):
    tb = pysam.TabixFile(filename)
    if genomic_range:
        it = tb.fetch(genomic_range)
    else:
        it = tb.fetch()
    bed_extracted_file="refGene.sort."+genomic_range+".bed.gz"
    bed_region=join(dirname(filename),bed_extracted_file)
    data=""
    with open(bed_region,"w") as tg:
        for row in it:
            data += '\t'.join(row)
        tg.write(data)
    return(bed_region)
