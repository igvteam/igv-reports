import unittest

from report.fasta import get_data


class FastaTest(unittest.TestCase):

    def test_all(self):

        data = get_data('data/finspector.fa')

        #print(str(data))

        self.assertTrue(data)

    def test_region(self):

        region = 'ACACA--STAC2:61-70'
        expected = 'ACAAATATTA'

        data = get_data('data/finspector.fa', region)


        self.assertEqual(expected, data)
