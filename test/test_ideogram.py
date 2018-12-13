import unittest

from report.ideogram import fetch_chromosome

class VcfTest(unittest.TestCase):

    def test_extract_chr(self):


        extracted = fetch_chromosome('data/cytoBandIdeo.txt', 'chr1')

        self.assertTrue(extracted)




