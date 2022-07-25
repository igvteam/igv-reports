import unittest
import pathlib
from igv_reports import datauri
from igv_reports.regions import parse_region

class FeatureFileTest(unittest.TestCase):


    def test_query(self):

        gff = str((pathlib.Path(__file__).parent / "data/minigenome/annotations.gtf.gz").resolve())
        region =  parse_region("minigenome:5000-6000")
        uri = datauri.file_to_data_uri(gff, 'gff', region)
        self.assertIsNotNone(uri)



    def test_noquery(self):

        file = str((pathlib.Path(__file__).parent / "data/minigenome/variants.bed").resolve())
        uri = datauri.file_to_data_uri(file)
        self.assertIsNotNone(uri)


