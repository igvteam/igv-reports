import unittest
import pathlib
from igv_reports import ideogram

class IdeogramTest(unittest.TestCase):

    def test_extract_chr(self):

        data_path = str((pathlib.Path(__file__).parent / 'data/cytoBandIdeo.txt').resolve())
        extracted = ideogram.get_data(data_path, {"chr": "chr1"})
        self.assertTrue(extracted.startswith('chr1'))



