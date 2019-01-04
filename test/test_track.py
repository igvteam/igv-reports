import unittest

import igv_reports.tracks


class TrackTest(unittest.TestCase):

    def test_all(self):

        path = 'data/minigenome/variants.vcf.gz'
        expected = 'variants.vcf'
        name = igv_reports.tracks.get_name(path)
        self.assertEqual(name, expected)

        format = igv_reports.tracks.infer_format(path)
        self.assertEqual('vcf', format)

        type = igv_reports.tracks.get_track_type(format)
        self.assertEqual('variant', type)



