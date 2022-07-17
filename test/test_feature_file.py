import unittest
import pathlib
import io
from igv_reports.feature import FeatureReader, _NonIndexed, parse_gff, parse_bed

class FeatureFileTest(unittest.TestCase):

    def test_fetch(self):

        gff = str((pathlib.Path(__file__).parent / "data/minigenome/annotations.gtf.gz").resolve())
        feature_file = FeatureReader(gff)
        content = feature_file.slice()
        features = parse_gff(io.StringIO(content))
        self.assertTrue(len(features) == 2106)


    def test_query(self):

        gff = str((pathlib.Path(__file__).parent / "data/minigenome/annotations.gtf.gz").resolve())
        feature_file = FeatureReader(gff)
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
        feature_file = _NonIndexed(gff)
        content = feature_file.slice()
        features = parse_gff(io.StringIO(content))
        self.assertTrue(len(features) == 2106)


    def test_nonindexed_query(self):

        gff = str((pathlib.Path(__file__).parent / "data/minigenome/annotations.gtf.gz").resolve())
        feature_file = _NonIndexed(gff)
        content = feature_file.slice({"chr": "minigenome", "start": 5000, "end": 6000})
        features = parse_gff(io.StringIO(content))
        self.assertEqual(len(features), 33)

        # features should be sorted by start position, and overlap the query interval
        last_start = 0
        for f in features:
            self.assertTrue(f.end >= 5000 and f.start <= 6000)
            self.assertTrue(f.start >= last_start)
            last_start = f.start



    def test_nongzipped_query(self):

        gff = str((pathlib.Path(__file__).parent / "data/minigenome/variants.bed").resolve())
        feature_file = FeatureReader(gff)
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
        bedpe = str((pathlib.Path(__file__).parent / "data/variants.pe.bed").resolve())
        feature_file = FeatureReader(bedpe)
        content = feature_file.slice(region, region2=region2, split_bool=True)
        features = parse_bed(io.StringIO(content))
        self.assertEqual(len(content.strip().split("\n")), 2)

