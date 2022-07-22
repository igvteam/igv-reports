import pysam
from featureTree import FeatureTree

def get_data(path, region = None):

    vcf = VcfReader(path)

    return vcf.slice(region)


class VcfReader:

    def __init__(self, path):

        self.file = pysam.VariantFile(path)
        self.feature_tree = None

    def slice(self, region = None, region2=None):

        vcf = self.file
        header = vcf.header

        fileString = str(header)

        if region == None:
            records = vcf.fetch()
        else:
            records = self.fetch(region['chr'], region['start'], region['end'])

        for rec in records:
            fileString += (str(rec))

        # Check for optional second region
        if region2 is not None:
            records2 = self.fetch(region2['chr'], region2['start'], region2['end'])
            for rec in records2:
                fileString += (str(rec))

        return fileString

    '''
    Wrap pysam fetch with workaround for non-indexed files
    '''
    def fetch(self, chr, start, end):

        vcf = self.file
        if vcf.index is not None:
            return vcf.fetch(chr, start, end)
        else:
            nodes =  self.get_feature_tree().query(chr, start, end)
            return list(map(lambda node: node.data.record, nodes))


    def get_feature_tree(self):

        if self.feature_tree is None:
            records = self.file.fetch()
            nodes = list(map(lambda rec: TreeNode(rec.contig, rec.pos - 1, rec.stop,  rec), records))
            self.feature_tree = FeatureTree(nodes)

        return self.feature_tree


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