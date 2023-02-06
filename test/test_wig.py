import unittest
import pathlib
import types

from igv_reports.wig import WigReader

class WIGTest(unittest.TestCase):

    def test_wig(self):

        region = {
            "chr": "chr22",
            "start": 42126499,
            "end": 42130810
        }

        wig_file_path = str((pathlib.Path(__file__).parent / "data/wig/variable_step.wig").resolve())
        wigreader = WigReader(wig_file_path)
        data = wigreader.slice(region)
        self.assertEqual(count_lines(data), 177)

    def test_wig_noregion(self):
        wig_file_path = str((pathlib.Path(__file__).parent / "data/wig/variable_step.wig").resolve())
        wigreader = WigReader(wig_file_path)
        data = wigreader.slice(region=None)
        self.assertEqual(count_lines(data), 1284)

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

        wig_file_path = str((pathlib.Path(__file__).parent / "data/wig/variable_step.wig").resolve())
        wigreader = WigReader(wig_file_path)
        data = wigreader.slice(region, region2)
        self.assertEqual(count_lines(data), 1268)


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

        wig_file_path = str((pathlib.Path(__file__).parent / "data/wig/variable_step.wig").resolve())
        wigreader = WigReader(wig_file_path)
        data = wigreader.slice(region, region2)
        self.assertEqual(count_lines(data), 64)
    
    def test_wig_mixed_step_same_chrom(self):
        region = {
            "chr": "chr19",
            "start": 49306691,
            "end": 49309000
        }

        wig_file_path = str((pathlib.Path(__file__).parent / "data/wig/mixed_step.wig").resolve())
        wigreader = WigReader(wig_file_path)
        data = wigreader.slice(region)
        self.assertEqual(count_lines(data), 10)


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

        wig_file_path = str((pathlib.Path(__file__).parent / "data/wig/variable_step.wig").resolve())
        wigreader = WigReader(wig_file_path)
        data = wigreader.slice(region, region2)
        self.assertEqual(count_lines(data), 1268)

def count_lines(data):
    return len([i for i in data.split('\n')])