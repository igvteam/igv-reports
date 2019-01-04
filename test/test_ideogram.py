import unittest

from igv_reports import ideogram

class IdeogramTest(unittest.TestCase):

    def test_extract_chr(self):

        extracted = ideogram.get_data('data/cytoBandIdeo.txt', {"chr": "chr1"})

        self.assertTrue(extracted)




