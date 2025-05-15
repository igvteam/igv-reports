import unittest
import pathlib
from igv_reports import fasta
from igv_reports.fasta import FastaReader
from igv_reports.twobit import TwoBitReader


class TwobitTest(unittest.TestCase):



    def test_region(self):

        expected = 'NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNACTCTATCTATCTATCTATCTATCTTTTTCCCCCCGGGGGGagagagagactc'
        reader = TwoBitReader('data/twobit/foo.2bit')
        data = reader.slice({
            "chr": "chr1",
            "start": 5 + 1,     # 1-based start
            "end": 100
        })

        self.assertTrue(data)
        self.assertEqual(expected, data)

    def test_remote(self):

        reader = FastaReader("https://igv.org/genomes/data/hg38/hg38.fa")
        data = reader.slice({"chr": "chr1",
                               "start": 100,
                               "end": 200})
        self.assertTrue(data)

        size = reader.get_reference_length("chr1")
        self.assertEqual(248956422, size)



    def test_remote_chrom(self):

        data = fasta.get_data("https://igv.org/genomes/data/hg38/hg38.fa",
                              {"chr": "chr5",
                               "start": 474979,
                               "end": 474998})
        self.assertEqual("ATCAGGCGGCAGAAGGTGCC", data)
