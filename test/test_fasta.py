import unittest

from report import fasta


class FastaTest(unittest.TestCase):

    def test_all(self):

        expected = '>ACACA--STAC2'

        data = fasta.get_data('data/finspector.fa')

        self.assertTrue(data.startswith(expected))

    def test_region(self):

        region = 'ACACA--STAC2:61-70'
        expected = 'ACAAATATTA'

        data = fasta.get_data('data/finspector.fa', region)

        print('\n')
        print(data)

        self.assertTrue(data)
        self.assertEqual(expected, data)
