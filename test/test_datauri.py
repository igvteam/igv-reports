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


    def test_media_type_of_text(self):

        # Text is gzipped before encoding
        uri = datauri.get_data_uri("hello")
        self.assertTrue(uri.startswith("data:application/gzip;base64,"), uri[:40])


    def test_media_type_of_gzipped_bytes(self):

        uri = datauri.get_data_uri(bytes([0x1f, 0x8b, 0x08, 0x00]))
        self.assertTrue(uri.startswith("data:application/gzip;base64,"), uri[:40])


    def test_media_type_of_plain_bytes(self):

        uri = datauri.get_data_uri(bytes([0x01, 0x02, 0x03]))
        self.assertTrue(uri.startswith("data:application/octet-stream;base64,"), uri[:40])
