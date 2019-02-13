import unittest

from igv_reports import tracks
from igv_reports import feature


class TrackTest(unittest.TestCase):

    def test_all(self):

        path = 'data/minigenome/variants.vcf.gz'
        expected = 'variants.vcf'
        name = tracks.get_name(path)
        self.assertEqual(name, expected)

        format = feature.infer_format(path)
        self.assertEqual('vcf', format)

        type = tracks.get_track_type(format)
        self.assertEqual('variant', type)



