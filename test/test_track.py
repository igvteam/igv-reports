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


class TrackConfigTest(unittest.TestCase):
    '''
    get_track_json_dict builds the igv.js track config for each --tracks argument.
    '''

    def test_alignment_track_shows_reads_kept_by_exclude_flags(self):

        # Alignments are filtered by samtools in bam.py according to --exclude-flags.  igv.js
        # hides duplicate and vendor failed reads by default, which would filter them a second
        # time, so the track config has to turn that off -- otherwise --exclude-flags 512
        # embeds the duplicates and the viewer hides them anyway.
        for path in ['x.bam', 'x.cram']:
            config = tracks.get_track_json_dict(path)
            self.assertEqual({"duplicate": False, "vendorFailed": False}, config.get("filter"),
                             f'{path} would be filtered a second time by igv.js')

    def test_alignment_track_defaults(self):

        config = tracks.get_track_json_dict('/data/sample.bam')
        self.assertEqual('sample', config["name"])
        self.assertEqual('/data/sample.bam', config["url"])
        self.assertEqual('alignment', config["type"])
        self.assertEqual('bam', config["format"])
        self.assertEqual(500, config["height"])

    def test_non_alignment_tracks_are_not_filtered(self):

        for path in ['x.vcf.gz', 'x.bed', 'x.wig']:
            self.assertNotIn("filter", tracks.get_track_json_dict(path))

    def test_variant_and_annotation_tracks(self):

        self.assertEqual('variant', tracks.get_track_json_dict('x.vcf')["type"])
        self.assertEqual('annotation', tracks.get_track_json_dict('x.bed')["type"])
