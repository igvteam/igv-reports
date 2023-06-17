import unittest

from igv_reports.stream import resource_exists

class StreamTest(unittest.TestCase):


    def test_resource_exists(self):

        # File exists
        exists = resource_exists("https://igv-genepattern-org.s3.amazonaws.com/test/reports/recalibrated.bam.bai")
        self.assertTrue(exists)

        # File does not exist
        exists = resource_exists("https://igv-genepattern-org.s3.amazonaws.com/test/reports/recalibrated.bai")
        self.assertFalse(exists)

        # Host does not exist
        exists = resource_exists("https://foo.bar/none")
        self.assertFalse(exists)

