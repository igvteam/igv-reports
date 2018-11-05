import unittest

from report import vcf


class VcfTest(unittest.TestCase):

    def test_get_header(self):

        expected = '>ACACA--STAC2'

        h = vcf.get_header('data/mut1/variants.vcf.gz')

        self.assertTrue(h)


    def test_get_variants(self):

        records = vcf.get_variants('data/mut1/variants.vcf.gz')

        for rec in records:

            print(rec)

        self.assertTre(records);


