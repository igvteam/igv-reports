import unittest

import pysam

import report.regions
from report import bam

class BAMTest(unittest.TestCase):

    def test_sam(self):


        bam_file_path = "/Users/jrobinso/igv-team Dropbox/James Robinson/projects/igv.js-reports/example/MI_viewer/recalibrated.bam"

        regions = ["chr5:474489-475489", "chr8:143923259-143924259"]

        alignments = bam.get_sam_data(bam_file_path, regions)

        self.assertTrue(alignments)

        #self.assertTrue(data.startswith(expected))


    def test_bam(self):

        bam_file_path = "/Users/jrobinso/igv-team Dropbox/James Robinson/projects/igv.js-reports/example/MI_viewer/recalibrated.bam"

        regions = ["chr5:474489-475489", "chr8:143923259-143924259"]

        bam_data = bam.get_data(bam_file_path, regions)

        self.assertTrue(bam_data)

        with open("test_slice.bam","w+b") as f:
            f.write(bam_data)


    def test_depth(self):


        bam_file_path = "/Users/jrobinso/igv-team Dropbox/James Robinson/projects/igv.js-reports/example/MI_viewer/recalibrated.bam"

        region = "chr5:474489-475489"

        depth = bam.get_depth(bam_file_path, region)

        self.assertTrue(depth)



    def test_merge_regions1(self):

        regions = ["chr1:1000-2000", "chr1:1005-3000", "chr1:2000-2500", "chr1:50000-60000", "chr2:200"]

        merged_regions = report.regions.merge_regions(regions)

        self.assertEquals(3, len(merged_regions))

        m = merged_regions[0]
        self.assertEquals('chr1', m['chr'])
        self.assertEquals(1000, m['start'])
        self.assertEquals(3000, m['end'])
