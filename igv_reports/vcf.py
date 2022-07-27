import pysam
from igv_reports.featureTree import FeatureTree
from igv_reports.chralias import build_aliastable, get_alias


class VcfReader:

    def __init__(self, path):

        self.file = pysam.VariantFile(path)
        self.feature_tree = None

        if self.file.index is None:
            records = self.file.fetch()
            nodes = list(map(lambda rec: TreeNode(rec.contig, rec.pos - 1, rec.stop, rec), records))
            self.feature_tree = FeatureTree(nodes)
            chrs = self.feature_tree.getchrs()
            self.aliastable = build_aliastable(chrs)

        else:
            # Build chr alias table from Contig lines in file header.  These are optional, but are usually there
            chrs = get_contigs(str(self.file.header))
            self.aliastable = build_aliastable(chrs)

    def slice(self, region=None, region2=None):

        vcf = self.file

        header = vcf.header

        fileString = str(header)

        if region == None:
            records = vcf.fetch()
        else:
            records = self.fetch(self.get_chrname(region['chr']), region['start'], region['end'])

            # Check for optional second region
            if region2 is not None:
                records2 = self.fetch(self.get_chrname(region2['chr']), region2['start'], region2['end'])
                for rec in records2:
                    records.append(rec)

        for rec in records:
            fileString += (str(rec))

        return fileString

    '''
    Wrap pysam fetch with workaround for non-indexed files. This exact logic is repeated in feature.py.
    '''

    def fetch(self, chr, start, end):

        if chr is None:
            return []

        vcf = self.file
        if vcf.index is not None:
            try:
                return vcf.fetch(chr, start, end)
            except ValueError:

                # Possible chr alias error (e.g. 1 vs chr1)
                try:
                    alias = get_alias(chr)
                    value = vcf.fetch(alias, start, end)
                    self.aliastable[chr] = alias
                    return value
                except ValueError:
                    self.aliastable[chr] = None
                    print(f'WARNING: No data with sequence name {chr} found in file {vcf.filename}')
                    return []

        else:
            nodes = self.feature_tree.query(chr, start, end)
            return list(filter(lambda rec: rec.stop >= start and rec.start <= end, map(lambda node: node.data.record, nodes)))

    def get_chrname(self, c):
        if c in self.aliastable:
            return self.aliastable[c]
        else:
            return c


class TreeNode:

    def __init__(self, chr, start, end, record):
        self.chr = chr
        self.start = start
        self.end = end
        self.record = record


def parse_info(record):
    info_str = str(record).split('\t')[7]
    fields = info_str.split(';')
    info_dict = {}
    for f in fields:
        kv = f.split('=')
        if len(kv) == 2:
            info_dict[kv[0]] = kv[1]
    return info_dict


def get_contigs(data):
    contigs = []
    lines = data.split('\n')
    for line in lines:
        if line.startswith('##contig'):
            idx1 = line.find("ID=")
            if idx1 > 0:
                idx2 = line.find(",")
                contigs.append(line[idx1 + 3:idx2])

    return contigs
