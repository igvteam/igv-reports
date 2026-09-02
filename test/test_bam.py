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
        args.subsample = None
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
        args.subsample = None
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

    def test_exclude_flags_retains_duplicate_reads(self):

        # The counts above say how many reads survive; this says which ones.  dups.bam holds
        # duplicate flagged reads and no vendor failed ones, so 1536 (the default) drops the
        # duplicates and 512 keeps every one of them.  This is what example_dups.html shows.
        bam_file_path = str((pathlib.Path(__file__).parent / "data/dups/dups.bam").resolve())
        region = {"chr": "1", "start": 658371, "end": 658460}

        args = types.SimpleNamespace()
        args.subsample = None

        args.exclude_flags = 1536
        data = BamReader("bam", bam_file_path, args).slice(region, sam=True)
        self.assertEqual(0, count_flagged(data, 0x400), 'default kept a duplicate read')

        args.exclude_flags = 512
        data = BamReader("bam", bam_file_path, args).slice(region, sam=True)
        self.assertEqual(count_alignments(data) - 73, count_flagged(data, 0x400))
        self.assertGreater(count_flagged(data, 0x400), 0, 'no duplicate reads to test with')


def count_flagged(data, mask):
    """Count alignment records whose SAM flag has every bit of mask set."""
    count = 0
    for line in data.split('\n'):
        if len(line) > 0 and not line.startswith("@"):
            if int(line.split('\t')[1]) & mask == mask:
                count += 1
    return count


def count_alignments(data):

    lines = data.split('\n')
    count = 0
    for line in lines:
        if len(line) > 0 and not line.startswith("@"):
            count += 1
    return count
