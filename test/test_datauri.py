import unittest
import pathlib
import io
from igv_reports.feature import FeatureReader, _NonIndexed, parse_gff
from igv_reports import datauri

class FeatureFileTest(unittest.TestCase):


    def test_query(self):

        gff = str((pathlib.Path(__file__).parent / "data/minigenome/annotations.gtf.gz").resolve())
        range =  "minigenome:5000-6000"
        uri = datauri.file_to_data_uri(gff, 'gff', range)
        self.assertIsNotNone(uri)



    def test_noquery(self):

        file = str((pathlib.Path(__file__).parent / "data/minigenome/variants.bed").resolve())
        uri = datauri.file_to_data_uri(file)
        self.assertIsNotNone(uri)


