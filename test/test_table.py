import unittest
import pathlib
from igv_reports.variant_table import VariantTable

class TableTest(unittest.TestCase):

    def test_get_header(self):

        vcf_path = str((pathlib.Path(__file__).parent / "data/minigenome/variants.vcf").resolve())
        table = VariantTable(vcf_path)
        self.assertEqual(len(table.variants), 28)



