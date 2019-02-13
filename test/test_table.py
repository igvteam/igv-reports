import unittest
import pathlib
from igv_reports import varianttable, bedtable

class TableTest(unittest.TestCase):

    def test_get_header(self):

        vcf_path = str((pathlib.Path(__file__).parent / "data/minigenome/variants.vcf").resolve())
        table = varianttable.VariantTable(vcf_path)
        self.assertEqual(len(table.variants), 28)

    def test_bedtable(self):

        bed_file = str((pathlib.Path(__file__).parent / "data/minigenome/variants.bed").resolve())
        table = bedtable.BedTable(bed_file)

        json = table.to_JSON()
        self.assertEqual(len(table.features), 4)
        self.assertTrue(json)

    def test_gfftable(self):

        gff = str((pathlib.Path(__file__).parent / "data/minigenome/annotations.gtf.gz").resolve())
        table = bedtable.BedTable(gff)
        json = table.to_JSON()
        self.assertTrue(len(table.features), 2106)
        self.assertTrue(json)






