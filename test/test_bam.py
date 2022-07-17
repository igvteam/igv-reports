import unittest
import pathlib

from igv_reports import bam

class BAMTest(unittest.TestCase):


    def test_bam(self):


        region = {
            "chr": "minigenome",
            "start": 4000,
            "end": 10000
        }

        bam_file_path = str((pathlib.Path(__file__).parent / "data/minigenome/alignments.bam").resolve())
        data = bam.get_data(bam_file_path, region)
        self.assertTrue(data)


    def test_bam_noregion(self):

        bam_file_path = str((pathlib.Path(__file__).parent / "data/minigenome/alignments.bam").resolve())
        data = bam.get_data(bam_file_path)
        self.assertTrue(data)


    def test_cram(self):
        region = {
            "chr": "minigenome",
            "start": 4000,
            "end": 10000
        }

        bam_file_path = str((pathlib.Path(__file__).parent / "data/minigenome/alignments.cram").resolve())
        ref_file_path = str((pathlib.Path(__file__).parent / "data/minigenome/minigenome.fa").resolve())

        reader = bam.BamReader(bam_file_path, ref_file_path);
        data = reader.slice(region)
        self.assertTrue(data)


    def test_multiple_bam_regions_diff_chrom(self):
        region = {
            "chr": "chr5",
            "start": 474989,
            "end": 474989
        }
        region2 = {
            "chr": "chr8",
            "start": 143923759,
            "end": 143923759
        }

        bam_file_path = str((pathlib.Path(__file__).parent / "data/recalibrated.bam").resolve())
        reader = bam.BamReader(bam_file_path);
        data = reader.slice(region, region2=region2, split_bool=True, sam=True)
        self.assertEqual(len(data.strip().split("\n")), 116)


    def test_multiple_bam_regions_same_chrom(self):
        region = {
            "chr": "chr5",
            "start": 474989,
            "end": 474989
        }
        region2 = {
            "chr": "chr5",
            "start": 181224474,
            "end": 181224474
        }

        bam_file_path = str((pathlib.Path(__file__).parent / "data/recalibrated.bam").resolve())
        reader = bam.BamReader(bam_file_path);
        data = reader.slice(region, region2=region2, split_bool=True, sam=True)
        self.assertEqual(len(data.strip().split("\n")), 93)

