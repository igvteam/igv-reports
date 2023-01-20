from igv_reports.chralias import build_aliastable

class WigReader:

    def __init__(self, filetype, filename):
        self.filtetype = filetype
        self.filename = filename

        self.seqnames, self.locations, self.seqheaders, self.file_header = parse_wig(filename)
        self.aliastable = build_aliastable(self.seqnames)

    def _region_slice(self, file_string, region = None):
        # factor out the slice to account for multiple regions in the slice function
        if region:
            seq_query = self.get_chrname(region['chr'])
            start = region['start']
            end = region['end']
            if seq_query in self.seqnames:
                header = self.seqheaders[seq_query]
                file_string += ' '.join(header)
                locs = self.locations[seq_query]
                for i, loc in enumerate(locs):
                    if int(loc[0]) >= start and int(loc[0]) <= end:
                        file_string += '\t'.join(loc)
        else:
            for seq, locs in self.locations.items():
                header = self.seqheaders[seq]
                file_string += ' '.join(header)
                for loc in locs:
                    file_string += '\t'.join(loc)
        return file_string

    def slice(self, region=None, region2=None):
        file_string = self.file_header
        if region:
            file_string = self._region_slice(file_string, region)
        if region2:
            file_string = self._region_slice(file_string, region2)
        if not region and not region2:
            file_string = self._region_slice(file_string)
        return file_string


    def get_chrname(self, c):
        if c in self.aliastable:
            return self.aliastable[c]
        else:
            return c


def parse_wig(filename):
    seqnames = []
    locs = {}
    seq_headers = {}
    with open(filename, 'r') as f:
        file_header = f.readline()
        for s in f.readlines():
            if s.startswith('fixedStep') or s.startswith('variableStep'):
                seqname = s.split('chrom=')[1].split(' ')[0]
                header = tuple(s.split(' '))
                seqnames.append(seqname)
                seq_headers[seqname] = header
                locs[seqname] = []
            elif s.startswith('track'):
                pass
            else:
                # append location and depth
                locs[seqname].append(s.split('\t'))
    return seqnames, locs, seq_headers, file_header
