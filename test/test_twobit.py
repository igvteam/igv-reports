import unittest
import pathlib

from igv_reports.twobit import TwoBitReader


class TwobitTest(unittest.TestCase):

    def setUp(self):
        self.path = str((pathlib.Path(__file__).parent / 'data/twobit/foo.2bit').resolve())

    def test_region(self):

        expected = 'NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNACTCTATCTATCTATCTATCTATCTTTTTCCCCCCGGGGGGagagagagactc'
        reader = TwoBitReader(self.path)
        data = reader.slice({
            "chr": "chr1",
            "start": 5 + 1,     # 1-based start
            "end": 100
        })

        self.assertTrue(data)
        self.assertEqual(expected, data)

    def test_region_as_locus_string(self):

        reader = TwoBitReader(self.path)
        self.assertEqual(reader.slice({"chr": "chr1", "start": 6, "end": 100}),
                         reader.slice("chr1:6-100"))

    def test_get_reference_length(self):

        reader = TwoBitReader(self.path)
        self.assertEqual(159, reader.get_reference_length("chr1"))

    def test_get_reference_length_alias(self):

        # The fixture names its sequence chr1; a query by its alias must still resolve
        reader = TwoBitReader(self.path)
        self.assertEqual(159, reader.get_reference_length("1"))


if __name__ == '__main__':
    unittest.main()
