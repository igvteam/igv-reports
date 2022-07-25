import unittest
import pathlib
from igv_reports.ideogram import IdeogramReader

class IdeogramTest(unittest.TestCase):

    def test_extract_chr(self):
        data_path = str((pathlib.Path(__file__).parent / 'data/hg19/cytoBandIdeo.txt').resolve())
        ideogram_reader = IdeogramReader(data_path)
        extracted = ideogram_reader.get_data("chr1")
        self.assertTrue(extracted.startswith('chr1'))

    def test_extract_chralias(self):
        data_path = str((pathlib.Path(__file__).parent / 'data/hg19/cytoBandIdeo.txt').resolve())
        ideogram_reader = IdeogramReader(data_path)
        extracted = ideogram_reader.get_data("2")
        self.assertTrue(extracted.startswith('chr2'))

    def test_multilocuas(self):

        data_path = str((pathlib.Path(__file__).parent / 'data/hg19/cytoBandIdeo.txt').resolve())
        ideogram_reader = IdeogramReader(data_path)
        ideo_string = ideogram_reader.get_data("chr18")
        ideo_string += ideogram_reader.get_data("chr19")

