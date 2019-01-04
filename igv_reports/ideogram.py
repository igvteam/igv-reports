

def get_data(cyto_file, region):

    result = ''
    chr = region['chr'] if region else None
    with open(cyto_file) as f:

        for line in f:

            tokens = line.split('\t')

            if chr == None or tokens[0] == chr:

                result += line

    return result
