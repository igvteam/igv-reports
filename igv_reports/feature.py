import pysam
from igv_reports.featureTree import FeatureTree
from igv_reports.chralias import get_alias
from igv_reports.stream import getstream

class Feature:

    def __init__(self, chr, start, end, text, name='', chr2=None, start2=None, end2=None):
        self.chr = chr
        self.start = start
        self.end = end
        self.chr2 = chr2
        self.start2 = start2
        self.end2 = end2
        self.text = text
        self.name = name

'''
Return an appropriate reader for the given path
'''
def get_featurereader(path):

    if path.endswith(".gz"):
        # Might be a tabix file
        try:
            return TabixFeatureReader(pysam.TabixFile(path))
        except:
            return FeatureReader(path)

    else:
        return FeatureReader(path)


'''
Tabix indexed file reader
'''

class TabixFeatureReader:

    def __init__(self, tabix):
        self.file = tabix
        self.aliastable = {}

    def slice(self, region=None, region2=None):

        tb = self.file
        if region is not None:
            chr = self.get_chrname(region["chr"])
            it = self._fetch(chr, region["start"], region["end"])
        else:
            it = tb.fetch()

        data = ""
        for row in it:
            data += row + '\n'

        if region2 is not None:
            chr = self.get_chrname(region2["chr"])
            it = self._fetch(chr, region2["start"], region2["end"])
            for row in it:
                data += row + '\n'

        return data

    def _fetch(self, chr, start, end):

        if chr is None:
            return []

        tb = self.file
        try:
            range_string = f'{chr}:{start}-{end}'
            return tb.fetch(range_string)

        except ValueError:
            # Possible chr alias error (e.g. 1 vs chr1)
            try:
                alias = get_alias(chr)
                range_string = f'{alias}:{start}-{end}'
                value = tb.fetch(range_string)
                self.aliastable[chr] = alias
                return value
            except ValueError:
                self.aliastable[chr] = None
                print(f'WARNING: No data with sequence name {chr} found in file {self.file.filename}')
                return []

    def get_chrname(self, c):
        if c in self.aliastable:
            return self.aliastable[c]
        else:
            return c


'''
Non-indexed file reader.  Emulates a tabix style query interface
'''

class FeatureReader:

    def __init__(self, file):

        self.file = file
        self.tree = None
        self.aliastable = {}

    def slice(self, region=None, region2=None):

        if region == None:
            f = None
            try:
                f = getstream(self.file)
                return f.read()
            finally:
                if f:
                    f.close()

        else:

            # If first time through read the entire file and create a queyable feature tree.
            if not self.tree:
                features = parse(self.file)
                for f in features:
                    if f.chr not in self.aliastable:
                        self.aliastable[get_alias(f.chr)] = f.chr
                self.tree = FeatureTree(features)

            features = []

            reference = self.get_chrname(region["chr"])
            start = region["start"]
            end = region["end"]
            feature_intervals = self.tree.query(reference, start, end)
            if feature_intervals:
                for i in feature_intervals:
                    features.append(i.data)

            if region2 is not None:
                reference = self.get_chrname(region2["chr"])
                start = region2["start"]
                end = region2["end"]
                feature_intervals = self.tree.query(reference, start, end)
                if feature_intervals:
                    for i in feature_intervals:
                        features.append(i.data)

        content = ''
        for f in features:
            content += f.text
        return content

    def get_chrname(self, c):
        if c in self.aliastable:
            return self.aliastable[c]
        else:
            return c


'''
A "mock reader" initialized with a list of bed features
'''

class MockReader:

    def __init__(self, features):
        self.features = features
        self.tree = FeatureTree(features)
        self.aliastable = {}
        for f in features:
            if f.chr not in self.aliastable:
                self.aliastable[get_alias(f.chr)] = f.chr

    def slice(self, region=None, region2=None):

        if region == None:
            return self.features

        else:

            features = []

            reference = self.get_chrname(region["chr"])
            start = region["start"]
            end = region["end"]
            feature_intervals = self.tree.query(reference, start, end)

            if feature_intervals:
                for i in feature_intervals:
                    features.append(i.data)

            if region2 is not None:
                reference = self.get_chrname(region2["chr"])
                start = region2["start"]
                end = region2["end"]
                feature_intervals = self.tree.query(reference, start, end)

                if feature_intervals:
                    for i in feature_intervals:
                        features.append(i.data)

            content = ''
            for f in features:
                chr = f.chr
                content += f"{chr}\t{f.start}\t{f.end}\n"
            return content

    def get_chrname(self, c):
        if c in self.aliastable:
            return self.aliastable[c]
        else:
            return c

def parse(path, format=None):
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
            return parse_bed(f)
        elif format == 'gff'  or format == 'gff3' or format == 'gtf':
            return parse_gff(f)
        elif format == 'tab':
            return parse_tab(f)
        elif format == 'bedpe':
            return parse_bedpe(f)
        elif format == 'refgene':
            return parse_refgene(f)
        else:
            raise Exception("Unknown file format: " + path)
    finally:
        if f:
            f.close()


def parse_bed(f):
    features = []
    for line in f:
        if not (line.startswith('#') or line.startswith('track') or line.startswith('browser')):
            tokens = line.rstrip('\n').rstrip('\r').split('\t')
            if len(tokens) >= 3:
                chr = tokens[0]
                start = int(tokens[1])
                end = int(tokens[2])
                name = tokens[3] if len(tokens) > 3 else ''
                features.append(Feature(chr, start, end, line, name))
    return features


def parse_refgene(f):
    features = []
    for line in f:
        if not (line.startswith('#') or line.startswith('track') or line.startswith('browser')):
            tokens = line.rstrip('\n').rstrip('\r').split('\t')
            if len(tokens) >= 3:
                chr = tokens[2]
                start = int(tokens[4])
                end = int(tokens[5])
                name = tokens[12] if len(tokens) > 12 else ''
                features.append(Feature(chr, start, end, line, name))
    return features


def parse_bedpe(f):
    features = []
    for line in f:
        if not (line.startswith('#') or line.startswith('track') or line.startswith('browser')):
            tokens = line.rstrip('\n').rstrip('\r').split('\t')
            if len(tokens) >= 6:
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
    elif filename.endswith(".bedpe"):
        return "bedpe"
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
