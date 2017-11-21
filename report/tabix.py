import pysam


def get_data(filename, genomic_range):
    tb = pysam.TabixFile(filename)
    if genomic_range:
        it = tb.fetch(genomic_range)
    else:
        it = tb.fetch()

    data = ""
    for row in it:
        data += '\t'.join(row)
