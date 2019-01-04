import unittest

from igv_reports import vcf
import pathlib

class VcfTest(unittest.TestCase):

    def test_get_variants(self):

        vcf_path = str((pathlib.Path(__file__).parent / "data/minigenome/variants.vcf").resolve())
        records = vcf.get_data(vcf_path)
        self.assertIsNotNone(records)




