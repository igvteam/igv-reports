import unittest

from igv_reports import bed
import pathlib

class BedTest(unittest.TestCase):

    def test_get_variants(self):

        bed_file = str((pathlib.Path(__file__).parent / "data/minigenome/variants.bed").resolve())
        records = bed.parse(bed_file)
        self.assertTrue(len(records) == 4)




