import unittest

from igv_reports import vcf


class VcfTest(unittest.TestCase):

    def test_get_variants(self):
        records = vcf.get_data('data/1kg/variants.vcf')
        self.assertIsNotNone(records)




