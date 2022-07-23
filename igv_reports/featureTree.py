
from intervaltree import IntervalTree

class FeatureTree:

    def __init__(self, featureList):

        self.featureMap = dict();

        for f in featureList:
            chr = f.chr
            tree = self.featureMap.get(chr)
            if tree == None:
                tree = IntervalTree()
                self.featureMap[chr] = tree
            tree[f.start:f.end] = f

    def query(self, chr, start, end):
        tree = self.featureMap.get(chr)
        if tree == None:
            return set()
        else:
            return tree[start:end]

    def getchrs(self):
        return self.featureMap.keys()
