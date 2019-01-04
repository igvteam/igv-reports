import unittest
import pathlib
from igv_reports import fasta


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

        print('\n')
        print(data)

        self.assertTrue(data)
        self.assertEqual(expected, data)
