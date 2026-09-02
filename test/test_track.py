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


    @unittest.expectedFailure
    def test_get_name_extensionless_path(self):
        # BUG tracks.py:42 -- `return filename[idx]` is missing the slice, so a path with a
        # directory but no extension yields only its first character.  Observed: 'm'
        self.assertEqual('mytrack', tracks.get_name('/data/mytrack'))


    @unittest.expectedFailure
    def test_get_name_period_before_last_slash(self):
        # BUG tracks.py:44 -- when the last '.' precedes the last '/' (a dotted host name, a
        # versioned directory) filename[idx:period] is an empty slice.  Observed: ''
        self.assertEqual('mytrack', tracks.get_name('http://host.com/mytrack'))


    @unittest.expectedFailure
    def test_get_name_trailing_slash(self):
        # BUG tracks.py:42 -- indexing one past the end raises rather than returning a name.
        # Observed: IndexError: string index out of range
        try:
            tracks.get_name('/data/')
        except IndexError:
            self.fail('get_name raised IndexError on a trailing slash')



