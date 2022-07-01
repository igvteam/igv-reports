from igv_reports import utils

def get_data(cyto_file, region):

    result = ''
    chr = region['chr'] if region else None
    with open(cyto_file) as f:

        for line in f:

            tokens = line.split('\t')

            if chr == None or tokens[0] == utils.decode_chrom(chr):
                if chr != None and "_" in chr:
                    result += utils.encode_chrom(line)
                else:
                    result += line

    return result
