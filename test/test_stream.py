import unittest

from igv_reports.stream import resource_exists

class StreamTest(unittest.TestCase):


    def test_resource_exists(self):

        # File exists
        exists = resource_exists("https://raw.githubusercontent.com/igvteam/igv-data/refs/heads/main/data/test/bam/small/gstt1_sample.bam.bai")
        self.assertTrue(exists)

        # File does not exist
        exists = resource_exists("https://raw.githubusercontent.com/igvteam/igv-data/refs/heads/main/data/test/bam/small/recalibrated.bai")
        self.assertFalse(exists)

        # Host does not exist
        exists = resource_exists("https://foo.bar/none")
        self.assertFalse(exists)

