from igv_reports.chralias import build_aliastable
from igv_reports.stream import getstream
from igv_reports.featureTree import FeatureTree
from igv_reports.feature import Feature

from collections import ChainMap

class WigReader:

    def __init__(self, file):
        self.file = file
        self.trees = None # use a dict of trees for each seq_header (i.e. to allow for multiple fixed/variable reagions per contig)

        self.header, self.features, self.seqnames  = parse_wig(file)
        self.trees = {k: FeatureTree(v) for k, v in self.features.items()}
        self.aliastable = build_aliastable(self.seqnames)
    
    def _query_trees(self, chrom, start, end):
        # query all trees for the region
        # return a list of features
        features = {}
        for seq, tree in self.trees.items():
            q = tree.query(chrom, start, end)
            if len(q) > 0:
                features[seq] = [f.data for f in q]
        return features

    def slice(self, region=None, region2=None):
        file_string = self.header
        features = []

        if region:
            reference = self.get_chrname(region["chr"])
            start = region["start"]
            end = region["end"]
            features.append(self._query_trees(reference, start, end))

            # Check for second region
            if region2:
                reference = self.get_chrname(region2["chr"])
                start = region2["start"]
                end = region2["end"]
                features.append(self._query_trees(reference, start, end))
        else:
            f = None
            try:
                f = getstream(self.file)
                return f.read()
            finally:
                if f:
                    f.close()
        for hdr, feat in ChainMap(*features).items():
            file_string += hdr
            for f in feat:
                file_string += f.text
        return file_string

    def get_chrname(self, c):
        if c in self.aliastable:
            return self.aliastable[c]
        else:
            return c

def parse_wig_header(header):
    # parse the key=value pairs in the header
    # return a dictionary
    header_dict = dict(ChainMap(*[{i.split('=')[0]: i.split('=')[1]} for i in header.split(' ')[1:]]))
    if 'span' not in header_dict:
        header_dict['span'] = 1
    return header_dict

def parse_wig(path):
    f = getstream(path)
    track_header = None
    step_header = None
    seq_features = {}
    seq_names = []
    current_type = None
    fixed_index = 0
    for s in f:
        if s.startswith('#'):
            continue
        elif s.startswith('track') and track_header is None:
            # this should only be on one (the first) line
            # ignores if it is redefined later in the file
            track_header = s
            continue
        elif s.startswith('fixedStep'):
            # chrom, start, step, span
            step_header_string = s
            step_header = parse_wig_header(step_header_string)
            current_type = 'fixed'
            seq_features[step_header_string] = []
            fixed_index = 0
            seq_names.append(step_header['chrom'])
            continue
        elif s.startswith('variableStep'):
            # need to get chrom and span (optional, default to 1)
            # positions are inferred from 
            step_header_string = s
            step_header = parse_wig_header(step_header_string)
            current_type = 'variable'
            seq_features[step_header_string] = []
            seq_names.append(step_header['chrom'])
            continue
        s_fields = s.strip().split()
        if current_type == 'fixed':
            start = int(step_header['start']) + (fixed_index * int(step_header['step']))
            fixed_index += 1
            end = start + int(step_header['span'])
            seq_features[step_header_string].append(Feature(step_header['chrom'], start, end, s, ''))
        elif current_type == 'variable':
            start = int(s_fields[0])
            end = start + int(step_header['span'])
            seq_features[step_header_string].append(Feature(step_header['chrom'], start, end, s, ''))
    #igv.js does not enforce the UCSC track line requirement for wig tracks
    if not track_header:
        track_header = ''
    #    raise Exception('Wig file is not properly formatted: missing track header in first line')
    return track_header, seq_features, list(set(seq_names))
