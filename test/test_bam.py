import unittest
import pathlib
import types

from igv_reports.bam import BamReader

class BAMTest(unittest.TestCase):


    def test_bam(self):

        region = {
            "chr": "minigenome",
            "start": 4000,
            "end": 10000
        }

        bam_file_path = str((pathlib.Path(__file__).parent / "data/minigenome/alignments.bam").resolve())
        bamreader = BamReader("bam", bam_file_path)
        data = bamreader.slice(region, sam=True)
        self.assertEqual(count_alignments(data), 923)

    def test_bam_noregion(self):

        bam_file_path = str((pathlib.Path(__file__).parent / "data/minigenome/alignments.bam").resolve())
        bamreader = BamReader("bam", bam_file_path)
        data = bamreader.slice(region=None, sam=True)
        self.assertEqual(count_alignments(data), 10212)


    def test_cram(self):
        region = {
            "chr": "minigenome",
            "start": 4000,
            "end": 10000
        }

        bam_file_path = str((pathlib.Path(__file__).parent / "data/minigenome/alignments.cram").resolve())
        ref_file_path = str((pathlib.Path(__file__).parent / "data/minigenome/minigenome.fa").resolve())

        args =  types.SimpleNamespace()
        args.fasta = ref_file_path
        reader = BamReader("cram", bam_file_path, args);
        data = reader.slice(region, sam=True)
        self.assertEqual(count_alignments(data), 923)


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

        bam_file_path = str((pathlib.Path(__file__).parent / "data/variants/recalibrated.bam").resolve())
        reader = BamReader("bam", bam_file_path);
        data = reader.slice(region, region2=region2, sam=True)
        self.assertEqual(count_alignments(data), 81)


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

        bam_file_path = str((pathlib.Path(__file__).parent / "data/variants/recalibrated.bam").resolve())
        reader = BamReader("bam", bam_file_path);
        data = reader.slice(region, region2=region2, sam=True)
        self.assertEqual(count_alignments(data), 58)

    def test_chralias(self):

        region = {
            "chr": "5",
            "start": 474989,
            "end": 474989
        }

        region2 = {
            "chr": "5",
            "start": 181224474,
            "end": 181224474
        }

        bam_file_path = str((pathlib.Path(__file__).parent / "data/variants/recalibrated.bam").resolve())
        reader = BamReader("bam", bam_file_path);
        data = reader.slice(region, region2, sam=True)
        self.assertEqual(count_alignments(data), 58)

    def test_exclude_flags(self):

        args =  types.SimpleNamespace()
        args.exclude_flags = 1536
        bam_file_path = str((pathlib.Path(__file__).parent / "data/dups/dups.bam").resolve())
        bamreader = BamReader("bam", bam_file_path, args)
        region = {
            "chr": "1",
            "start": 658371,
            "end": 658460
        }
        data = bamreader.slice(region, sam=True)
        self.assertEqual(count_alignments(data), 73)

        args.exclude_flags = 1024
        bamreader = BamReader("bam", bam_file_path, args)
        data = bamreader.slice(region, sam=True)
        self.assertEqual(count_alignments(data), 73)

        args.exclude_flags = 0
        bamreader = BamReader("bam", bam_file_path, args)
        data = bamreader.slice(region, sam=True)
        self.assertEqual(count_alignments(data), 121)

        args.exclude_flags = 512
        bamreader = BamReader("bam", bam_file_path, args)
        data = bamreader.slice(region, sam=True)
        self.assertEqual(count_alignments(data), 121)



def count_alignments(data):

    lines = data.split('\n')
    count = 0
    for line in lines:
        if len(line) > 0 and not line.startswith("@"):
            count += 1
    return count
