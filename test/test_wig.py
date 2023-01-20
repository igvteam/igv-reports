import unittest
import pathlib
import types

from igv_reports.coverage import WigReader

class WIGTest(unittest.TestCase):

    def test_wig(self):

        region = {
            "chr": "chr22",
            "start": 42126499,
            "end": 42130810
        }

        wig_file_path = str((pathlib.Path(__file__).parent / "data/coverage/NA12878.CYPs.wig").resolve())
        wigreader = WigReader("wig", wig_file_path)
        data = wigreader.slice(region)
        self.assertEqual(count_depths(data), 173)

    def test_bam_noregion(self):
        wig_file_path = str((pathlib.Path(__file__).parent / "data/coverage/NA12878.CYPs.wig").resolve())
        wigreader = WigReader("wig", wig_file_path)
        data = wigreader.slice(region=None)
        self.assertEqual(count_depths(data), 1280)

    def test_multiple_wig_regions_diff_chrom(self):
        region = {
            "chr": "chr7",
            "start": 99756967,
            "end": 99784184
        }
        region2 = {
            "chr": "chr22",
            "start": 42126499,
            "end": 42130810
        }

        wig_file_path = str((pathlib.Path(__file__).parent / "data/coverage/NA12878.CYPs.wig").resolve())
        wigreader = WigReader("wig", wig_file_path)
        data = wigreader.slice(region, region2)
        self.assertEqual(count_depths(data), 1262)


    def test_multiple_wig_regions_same_chrom(self):
        region = {
            "chr": "chr22",
            "start": 42126499,
            "end": 42128000
        }
        region2 = {
            "chr": "chr22",
            "start": 42128000,
            "end": 42130810
        }

        wig_file_path = str((pathlib.Path(__file__).parent / "data/coverage/NA12878.CYPs.wig").resolve())
        wigreader = WigReader("wig", wig_file_path)
        data = wigreader.slice(region, region2)
        self.assertEqual(count_depths(data), 173)


    def test_chralias(self):
        region = {
            "chr": "7",
            "start": 99756967,
            "end": 99784184
        }
        region2 = {
            "chr": "22",
            "start": 42126499,
            "end": 42130810
        }

        wig_file_path = str((pathlib.Path(__file__).parent / "data/coverage/NA12878.CYPs.wig").resolve())
        wigreader = WigReader("wig", wig_file_path)
        data = wigreader.slice(region, region2)
        self.assertEqual(count_depths(data), 1262)




def count_depths(data):
    return len([i for i in data.split('\n') if i.split('\t')[0].isnumeric()])