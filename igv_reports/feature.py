import gzip
import io
import pysam
import requests
from intervaltree import IntervalTree


class Feature:

    def __init__(self, chr, start, end, text, name='', chr2='', start2=0, end2=0):
        self.chr = chr
        self.start = start
        self.end = end
        self.chr2 = chr2
        self.start2 = start2
        self.end2 = end2
        self.text = text
        self.name = name


class FeatureReader:

    def __init__(self, path):

        tabix = None
        if path.endswith(".gz"):
            # Might be a tabix file
            try:
                tabix = pysam.TabixFile(path)
            except:
                tabix = None

        if tabix:
            self.reader = _Tabix(tabix)
        else:
            self.reader = _NonIndexed(path)

    def slice(self, region=None, region2=None, split_bool=False):
        return self.reader.slice(region, region2, split_bool)


class _Tabix:

    def __init__(self, tabix):
        self.file = tabix

    def slice(self, region=None, region2=None, split_bool=False):

        tb = self.file
        if region:
            range_string = region['chr'] + ":" + str(region['start']) + "-" + str(region['end'])
            it = tb.fetch(range_string)
        else:
            it = tb.fetch()

        data = ""
        for row in it:
            data += row + '\n'

        if not split_bool:
            return data
        else:
            if region2:
                range_string = region2['chr'] + ":" + str(region2['start']) + "-" + str(region2['end'])
                it = tb.fetch(range_string)
            else:
                it = tb.fetch()

            for row in it:
                data += row + '\n'

            return data



## Implement a pysam/tabix style inteface for non-indexed files
class _NonIndexed:

    def __init__(self, file):

        self.file = file
        self.tree = None

    def slice(self, region=None, region2=None, split_bool=False):

        if region == None:
            f = None
            try:
                f = getstream(self.file)
                return f.read()
            finally:
                if f:
                    f.close()

        else:
            if not self.tree:
                features = parse(self.file)
                self.tree = FeatureTree(features)

            def sortFunc(f):
                    return f.start

            reference = region["chr"]
            start = region["start"]
            end = region["end"]
            feature_intervals = self.tree.query(reference, start, end)

            features = []
            if feature_intervals:
                for i in feature_intervals:
                    features.append(i.data)

        if not split_bool:
            features = sorted(features, key=sortFunc)
            content = ''
            for f in features:
                content += f.text
            return content
        else:
            if region2 == None:
                f = None
                try:
                    f = getstream(self.file)
                    return f.read()
                finally:
                    if f:
                        f.close()

            else:
                if not self.tree:
                    features = parse(self.file)
                    self.tree = FeatureTree(features)

                reference = region2["chr"]
                start = region2["start"]
                end = region2["end"]
                feature_intervals = self.tree.query(reference, start, end)

                if feature_intervals:
                    for i in feature_intervals:
                        features.append(i.data)

                features = sorted(features, key=sortFunc)
                content = ''
                for f in features:
                    content += f.text
                return content


# This class is initialized with a list of "bed like" features, mocks an indexed file reader
class MockReader:

    def __init__(self, features):

        self.tree = FeatureTree(features)

    def slice(self, region=None, region2=None, split_bool=False):

        reference = region["chr"]
        start = region["start"]
        end = region["end"]
        feature_intervals = self.tree.query(reference, start, end)

        def sortFunc(f):
            return f.start

        features = []
        if feature_intervals:
            for i in feature_intervals:
                features.append(i.data)

        if not split_bool:
            features = sorted(features, key=sortFunc)
            content = ''
            for f in features:
                content += f"{f.chr}\t{f.start}\t{f.end}\n"
            return content
        else:
            reference = region2["chr"]
            start = region2["start"]
            end = region2["end"]
            feature_intervals = self.tree.query(reference, start, end)

            features = []
            if feature_intervals:
                for i in feature_intervals:
                    features.append(i.data)

            features = sorted(features, key=sortFunc)
            for f in features:
                chr = f.chr
                content += f"{chr}\t{f.start}\t{f.end}\n"
            return content



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


def get_data(filename, region=None):
    reader = FeatureReader(filename)
    return reader.slice(region)


def parse(path, format=None, split_bool=False):
    '''
    Parse a feature file and return an array of feature objects.  Supported formats are bed, gff, and gtf.
    :param path: Path to feature file, which can be local or url
    :param format: File format, bed | gtf | gff
    :param split_bool: Boolean specifying whether view is multi locus or not
    :return: List of feature objects {chr, start, end, text, name}
    '''

    f = None
    try:
        f = getstream(path)
        if not format:
            format = infer_format(path)
        if format == 'bed':
            return parse_bed(f, split_bool)
        elif format == 'gff' or format == 'gtf':
            return parse_gff(f)
        elif format == 'tab':
            return parse_tab(f)
        else:
            raise Exception("Unknown file format: " + path)
    finally:
        if f:
            f.close()


def parse_bed(f, split_bool=False):
    features = []
    for line in f:
        if not (line.startswith('#') or line.startswith('track') or line.startswith('browser')):
            tokens = line.rstrip('\n').rstrip('\r').split('\t')
            if len(tokens) > 2:
                if not split_bool:
                    chr = tokens[0]
                    start = int(tokens[1])
                    end = int(tokens[2])
                    name = tokens[3] if len(tokens) > 3 else ''
                    features.append(Feature(chr, start, end, line, name))
                else:
                    chr = tokens[0]
                    start = int(tokens[1])
                    end = int(tokens[2])
                    chr2 = tokens[3]
                    start2 = int(tokens[4])
                    end2 = int(tokens[5])
                    name = tokens[6] if len(tokens) > 6 else ''
                    features.append(Feature(chr, start, end, line, name, chr2, start2, end2))
    return features


def parse_gff(f):
    features = []
    for line in f:
        if not (line.startswith('#') or line.startswith('track') or line.startswith('browser')):
            tokens = line.rstrip('\n').rstrip('\r').split('\t')
            # if we encounter a blank or malformed line (no start and end coords), skip it
            if len(tokens) < 5:
                continue
            chr = tokens[0]
            start = int(tokens[3]) - 1
            end = int(tokens[4])
            name = ''
            features.append(Feature(chr, start, end, line, name))

    return features


def parse_tab(f):
    rows = []
    for line in f:
        if not (line.startswith('#') or line.startswith('track') or line.startswith('browser')):
            tokens = line.rstrip('\n').rstrip('\r').split('\t')
            if len(tokens) > 2:
                rows.append(tokens)
    return rows


def infer_format(filename):
    '''
    Infer the genomic file format from the filename.  First known formats are checked.  Next presenece of
    the magic string "refgene" in the filename is checked for UCSC refgene files.  This is a legacy
    IGV convention.  The order is important, a recognized extension wins.
    NOTE: Formats are for output data uris.  CRAM format is converted to BAM before output.
    :param filename:
    :return:
    '''
    filename = filename.lower()
    if (filename.endswith(".gz")):
        filename = filename[:-3]

    if filename.endswith(".bam"):
        return "bam"
    if filename.endswith(".cram"):
        return "cram"
    elif filename.endswith(".vcf"):
        return "vcf"
    elif filename.endswith(".bed"):
        return "bed"
    elif filename.endswith(".gff") or filename.endswith(".gff3"):
        return "gff"
    elif filename.endswith(".gtf"):
        return "gtf"
    elif filename.find("refgene"):
        return "refgene"
    else:
        idx = filename.rfind(".")
        if idx > 0:
            return filename[idx + 1:]
        else:
            return None
        idx = filename.rfind(".")
        if idx > 0:
            return filename[idx + 1:]
        else:
            return None


def getstream(file):
    # TODO -- gcs

    if file.startswith('http://') or file.startswith('https://'):
        response = requests.get(file)
        status_code = response.status_code  # TODO Do something with this

        if file.endswith('.gz'):
            content = response.content
            text = gzip.decompress(content).decode('utf-8')
        else:
            text = response.text
        f = io.StringIO(text)
        return text

    elif file.endswith('.gz'):
        f = gzip.open(file, mode='rt')

    else:
        f = open(file, encoding='UTF-8')

    return f
