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


    def test_get_name(self):

        # get_name supplies the display name of every track in the report
        self.assertEqual('x', tracks.get_name('x.bam'))
        self.assertEqual('x', tracks.get_name('/data/x.bam'))
        self.assertEqual('x', tracks.get_name('http://host.com/x.vcf'))
        self.assertEqual('mytrack', tracks.get_name('mytrack'))


    def test_get_name_extensionless_path(self):
        # A path with a directory but no extension keeps its whole base name
        self.assertEqual('mytrack', tracks.get_name('/data/mytrack'))


    def test_get_name_period_before_last_slash(self):
        # The extension is looked for in the base name, so a dotted host name or a versioned
        # directory does not swallow it
        self.assertEqual('mytrack', tracks.get_name('http://host.com/mytrack'))


    def test_get_name_trailing_slash(self):
        # A trailing slash yields an empty name rather than raising
        try:
            tracks.get_name('/data/')
        except IndexError:
            self.fail('get_name raised IndexError on a trailing slash')



