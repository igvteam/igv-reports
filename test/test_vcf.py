import unittest

from igv_reports.vcf import VcfReader
import pathlib

def get_data(path, region = None):
    vcf = VcfReader(path)
    return vcf.slice(region)


class VcfTest(unittest.TestCase):

    def test_getvariants(self):

        path = str((pathlib.Path(__file__).parent / "data/minigenome/variants.vcf").resolve())
        region = {"chr": "minigenome", "start": 87944 - 1, "end": 87944 + 1}
        data = get_data(path, region)
        count = count_variants(data)
        self.assertEqual(count, 1)

        path = str((pathlib.Path(__file__).parent / "data/minigenome/variants.vcf.gz").resolve())
        region = {"chr": "minigenome", "start": 87944 - 1, "end": 87944 + 1}
        data = get_data(path, region)
        count = count_variants(data)
        self.assertEqual(count, 1)

        path = str((pathlib.Path(__file__).parent / "data/minigenome/variants.bcf").resolve())
        region = {"chr": "minigenome", "start": 87944 - 1, "end": 87944 + 1}
        data = get_data(path, region)
        count = count_variants(data)
        self.assertEqual(count, 1)

    def test_remote(self):

        path = "https://s3.amazonaws.com/igv.org.test/reports/variants/cancer.vcf.gz"
        region = {"chr": "chr17", "start": 7673767, "end": 43071077}
        data = get_data(path, region)
        count = count_variants(data)
        self.assertTrue(count > 0)

    def test_multilocus(self):
        path = str((pathlib.Path(__file__).parent / "../test/data/variants/SKBR3_Sniffles_variants_tra.vcf").resolve())
        vcf = VcfReader(path)
        region = {"chr": "8", "start": 77706277-1, "end": 77706277+1}
        region2 = {"chr": "14", "start": 50256582-1, "end": 50256582+1}
        data = vcf.slice(region, region2)
        count = count_variants(data)
        self.assertEqual(count, 2)

    def test_alias(self):
        path = str((pathlib.Path(__file__).parent / "../test/data/variants/SKBR3_Sniffles_variants_tra.vcf").resolve())
        vcf = VcfReader(path)
        region = {"chr": "chr8", "start": 77706277-1, "end": 77706277+1}
        region2 = {"chr": "chr14", "start": 50256582-1, "end": 50256582+1}
        data = vcf.slice(region, region2)
        count = count_variants(data)
        self.assertEqual(count, 2)

    def test_missingchr(self):
        path = str((pathlib.Path(__file__).parent / "../test/data/variants/SKBR3_Sniffles_variants_tra.vcf").resolve())
        vcf = VcfReader(path)
        region = {"chr": "99", "start": 77706277-1, "end": 77706277+1}
        data = vcf.slice(region)
        count = count_variants(data)
        self.assertEqual(count, 0)

    def test_notindexed(self):
        path = str((pathlib.Path(__file__).parent / "../test/data/variants/1kg_phase3_sites.vcf").resolve())
        vcf = VcfReader(path)
        region = {"chr": "chr22", "start": 50173573-1, "end": 50173573+1}
        data = vcf.slice(region)
        count = count_variants(data)
        self.assertEqual(2, count)


    def test_tabix(self):
        path = str((pathlib.Path(__file__).parent / "../test/data/variants/1kg_phase3_sites.vcf.gz").resolve())
        vcf = VcfReader(path)
        region = {"chr": "chr22", "start": 50173573-1, "end": 50173573}
        data = vcf.slice(region)
        count = count_variants(data)
        self.assertEqual(2, count)

    def test_tabix_alias(self):
        path = str((pathlib.Path(__file__).parent / "../test/data/variants/1kg_phase3_sites.vcf.gz").resolve())
        vcf = VcfReader(path)
        region = {"chr": "22", "start": 50173573-1, "end": 50173573}
        data = vcf.slice(region)
        count = count_variants(data)
        self.assertEqual(2, count)

    def test_tabix_missingchr(self):
        path = str((pathlib.Path(__file__).parent / "../test/data/variants/1kg_phase3_sites.vcf.gz").resolve())
        vcf = VcfReader(path)
        region = {"chr": "99", "start": 50173573-1, "end": 50173573}
        data = vcf.slice(region)
        count = count_variants(data)
        self.assertEqual(count, 0)

def count_variants(data):

    lines = data.split('\n')
    count = 0
    header_read = False
    for line in lines:
        if header_read and len(line) > 0:
            print(line)
            count+=1
        else:
            if line.startswith("#CHROM"):
                header_read = True
    return count
