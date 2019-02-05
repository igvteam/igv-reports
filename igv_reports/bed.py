import io
import gzip
from .feature import Feature



def parse(bed_file):

    features = []

    if bed_file.endswith('.gz'):
        f = gzip.open(bed_file, mode='rt')
    else:
        f = open(bed_file, encoding='UTF-8')

    try:
        for line in f:
           if not (line.startswith('#') or line.startswith('track') or line.startswith('browser')):
               line = line.rstrip("\n")
               tokens = line.split('\t')
               chr = tokens[0]
               start = int(tokens[1])
               end = int(tokens[2])
               name = tokens[3] if len(tokens) > 3 else ''
               features.append(Feature(chr, start, end, name))

    finally:
        f.close()


    return features









