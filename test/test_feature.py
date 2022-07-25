import unittest
import pathlib
import io
from igv_reports.feature import get_featurereader, FeatureReader, parse_gff, parse_bed


class FeatureFileTest(unittest.TestCase):

    def test_fetch(self):

        gff = str((pathlib.Path(__file__).parent / "data/minigenome/annotations.gtf.gz").resolve())
        feature_file = get_featurereader(gff)
        content = feature_file.slice()
        features = parse_gff(io.StringIO(content))
        self.assertTrue(len(features) == 2106)

    def test_tabix(self):

        gff = str((pathlib.Path(__file__).parent / "data/minigenome/annotations.gtf.gz").resolve())
        feature_file = get_featurereader(gff)
        content = feature_file.slice({"chr": "minigenome", "start": 5000, "end": 6000})
        features = parse_gff(io.StringIO(content))
        self.assertEqual(len(features), 33)

        # features should be sorted by start position, and overlap the query interval
        last_start = 0
        for f in features:
            self.assertTrue(f.end >= 5000 and f.start <= 6000)
            self.assertTrue(f.start >= last_start)
            last_start = f.start

    def test_nonindexed_fetch(self):

        gff = str((pathlib.Path(__file__).parent / "data/minigenome/annotations.gtf.gz").resolve())
        feature_file = FeatureReader(gff)
        content = feature_file.slice()
        features = parse_gff(io.StringIO(content))
        self.assertTrue(len(features) == 2106)

    def test_nonindexed_query(self):

        gff = str((pathlib.Path(__file__).parent / "data/minigenome/annotations.gtf.gz").resolve())
        feature_file = FeatureReader(gff)
        content = feature_file.slice({"chr": "minigenome", "start": 5000, "end": 6000})
        features = parse_gff(io.StringIO(content))
        self.assertEqual(len(features), 33)

        # features should be sorted by start position, and overlap the query interval
        for f in features:
            self.assertTrue(f.end >= 5000 and f.start <= 6000)

    def test_nongzipped_query(self):

        gff = str((pathlib.Path(__file__).parent / "data/minigenome/variants.bed").resolve())
        feature_file = get_featurereader(gff)
        content = feature_file.slice({"chr": "minigenome", "start": 4000, "end": 7000})
        features = parse_bed(io.StringIO(content))
        self.assertEqual(len(features), 3)

    def test_non_gzipped_query_bedpe(self):

        region = {
            "chr": "chr5",
            "start": 470000,
            "end": 480000
        }
        region2 = {
            "chr": "chr5",
            "start": 180000000,
            "end": 190000000
        }
        bedpe = str((pathlib.Path(__file__).parent / "data/variants.bedpe").resolve())
        feature_file = get_featurereader(bedpe)
        content = feature_file.slice(region, region2=region2)
        features = parse_bed(io.StringIO(content))
        self.assertEqual(len(content.strip().split("\n")), 2)

    def test_multilocus(self):
        path = str((pathlib.Path(__file__).parent / "data/hg38/refGene.txt").resolve())
        feature_reader = get_featurereader(path)
        region = {"chr": "chr5", "start": 470454, "end": 480892}
        region2 = {"chr": "chr7", "start": 55019020, "end": 55019277}
        data = feature_reader.slice(region, region2)
        self.assertEqual(12, count_features(data))

    def test_tabix(self):
        path = str((pathlib.Path(__file__).parent / "data/hg38/refGene.txt.gz").resolve())
        feature_reader = get_featurereader(path)
        region = {"chr": "5", "start": 470454, "end": 480892}
        region2 = {"chr": "7", "start": 55019020, "end": 55019277}
        data = feature_reader.slice(region, region2)
        self.assertEqual(12, count_features(data))

    def test_alias(self):
        path = str((pathlib.Path(__file__).parent / "data/hg38/refGene.txt").resolve())
        feature_reader = get_featurereader(path)
        region = {"chr": "8", "start": 470454, "end": 480892}
        data = feature_reader.slice(region)
        self.assertEqual(2, count_features(data))

    '''
    Test a tabix query for a chromosome that is not present in the data file.
    This should return an array of size zero
    '''
    def test_missingchr(self):
        path = str((pathlib.Path(__file__).parent / "data/hg38/refGene.txt").resolve())
        feature_reader = get_featurereader(path)
        region = {"chr": "999", "start": 470454, "end": 480892}
        data = feature_reader.slice(region)
        self.assertEqual(0, count_features(data))

    '''
    Test a tabix query for a chromosome that is not present in the data file.   
    This should return an array of size zero, and log a warning to the console.
    '''
    def test_tabix_missingchr(self):
        path = str((pathlib.Path(__file__).parent / "data/hg38/refGene.txt.gz").resolve())
        feature_reader = get_featurereader(path)
        region = {"chr": "999", "start": 470454, "end": 480892}
        data = feature_reader.slice(region)
        self.assertEqual(0, count_features(data))

    # Note: the following test is slow
    # def test_remote_tabix(self):
    #     path = "https://s3.amazonaws.com/igv.org.genomes/hg38/annotations/gencode.v28.basic.annotation.sorted.gtf.gz"
    #     feature_reader = FeatureReader(path)
    #     region = {"chr": "5", "start": 470454, "end": 480892}
    #     region2 = {"chr": "7", "start": 55019020, "end": 55019277}
    #     data = feature_reader.slice(region, region2)
    #     print(data)
    #     self.assertEqual(count_features(data), 101)


def count_features(data):
    lines = data.split('\n')
    count = 0
    for line in lines:
        if not line.startswith('#') and len(line) > 0:
            count += 1
    return count
