import unittest
import pathlib
from igv_reports import bed
from igv_reports import bed_table


class BedTest(unittest.TestCase):

    def test_get_features(self):

        bed_file = str((pathlib.Path(__file__).parent / "data/minigenome/variants.bed").resolve())
        records = bed.parse(bed_file)
        self.assertTrue(len(records) == 4)

    def test_get_gzipped_features(self):

        bed_file = str((pathlib.Path(__file__).parent / "data/minigenome/variants.bed.gz").resolve())
        records = bed.parse(bed_file)
        self.assertTrue(len(records) == 4)

    def test_get_table(self):

        bed_file = str((pathlib.Path(__file__).parent / "data/minigenome/variants.bed").resolve())
        table = bed_table.BedTable(bed_file)
        json = table.to_JSON()
        self.assertTrue(json)




