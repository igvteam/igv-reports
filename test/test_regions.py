import unittest

from igv_reports import regions


class RegionsTest(unittest.TestCase):

    def test_merge_regions(self):

        rlist = ["chr1:1000-2000", "chr1:1005-3000", "chr1:2000-2500", "chr1:50000-60000", "chr2:200"]

        merged_regions = regions.merge_regions(rlist)

        self.assertEqual(3, len(merged_regions))

        m = merged_regions[0]
        self.assertEqual('chr1', m['chr'])
        self.assertEqual(1000, m['start'])
        self.assertEqual(3000, m['end'])
