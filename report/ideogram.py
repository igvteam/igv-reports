

def fetch_chromosome(cyto_file, chr):

    result = ''
    with open(cyto_file) as f:

        for line in f:

            tokens = line.split('\t')

            if tokens[0] == chr:

                result += line

    return result
