import unittest
import pathlib
from igv_reports import fasta
from igv_reports.fasta import FastaReader


class FastaTest(unittest.TestCase):

    def test_all(self):

        expected = '>ACACA--STAC2'

        fasta_path = str((pathlib.Path(__file__).parent / 'data/finspector.fa').resolve())
        data = fasta.get_data(fasta_path)

        self.assertTrue(data.startswith(expected))

    def test_region(self):

        region = 'ACACA--STAC2:61-70'
        expected = 'ACAAATATTA'

        data = fasta.get_data('data/finspector.fa', region)

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
