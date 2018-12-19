import unittest

import report.tracks


class TrackTest(unittest.TestCase):

    def test_all(self):

        path = 'data/minigenome/variants.vcf.gz'
        expected = 'variants.vcf'
        name = report.tracks.get_name(path)
        self.assertEqual(name, expected)

        format = report.tracks.infer_format(path)
        self.assertEqual('vcf', format)

        type = report.tracks.get_track_type(format)
        self.assertEqual('variant', type)

        self.assertTrue(report.tracks.is_tabix(path))


