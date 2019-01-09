import unittest

import pysam

import igv_reports.regions
from igv_reports import bam

class RegionsTest(unittest.TestCase):

    def test_merge_regions(self):

        regions = ["chr1:1000-2000", "chr1:1005-3000", "chr1:2000-2500", "chr1:50000-60000", "chr2:200"]

        merged_regions = igv_reports.regions.merge_regions(regions)

        self.assertEquals(3, len(merged_regions))

        m = merged_regions[0]
        self.assertEquals('chr1', m['chr'])
        self.assertEquals(1000, m['start'])
        self.assertEquals(3000, m['end'])