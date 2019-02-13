import unittest

from igv_reports import vcf
import pathlib

class VcfTest(unittest.TestCase):

    def test_getvariants(self):

        path = str((pathlib.Path(__file__).parent / "data/minigenome/variants.vcf").resolve())
        data = vcf.get_data(path)
        self.assertIsNotNone(data)


    def test_getvariants_remote(self):

        path = "https://s3.amazonaws.com/igv.org.test/reports/variants/cancer.vcf.gz"
        region = {"chr": "chr17", "start": 7673767, "end": 43071077}
        data = vcf.get_data(path, region)
        self.assertIsNotNone(data)

