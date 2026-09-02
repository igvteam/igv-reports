import re
import unittest
import types

from igv_reports.feature import Feature
from igv_reports.report import create_locus_dict, locus_string

# Coordinates are matched loosely -- signed and fractional -- so that a malformed locus is
# reported by the assertion that cares about it rather than by an error in this helper.
LOCUS_PATTERN = re.compile(r'^(?P<chr>.+):(?P<start>-?[\d.]+)(?:-(?P<end>-?[\d.]+))?$')


def parse_locus(locus):
    """Split 'chr:start-end' or 'chr:pos' into (chr, start, end) strings."""
    match = LOCUS_PATTERN.match(locus)
    if match is None:
        raise AssertionError(f'unparseable locus {locus!r}')
    start = match.group('start')
    return match.group('chr'), start, (match.group('end') or start)


class LocusStringTest(unittest.TestCase):
    '''
    locus_string converts a 0-based half-open feature interval to the 1-based inclusive
    locus string used as the initial view of every report.  Called from create_session_dict
    (report.py:321) and create_locus_dict (report.py:472).
    '''

    def test_snv_no_window(self):
        # A 1bp feature collapses to a single position
        self.assertEqual('chr1:101', locus_string('chr1', 100, 101, None))

    def test_range_no_window(self):
        self.assertEqual('chr1:101-200', locus_string('chr1', 100, 200, None))

    def test_no_start(self):
        # Features without coordinates (e.g. fusion json) yield a bare chromosome name
        self.assertEqual('chr1', locus_string('chr1', None, None, None))

    def test_window_is_integral(self):
        # A genomic locus has whole coordinates; window / 2 must not introduce a fraction
        for window in [41, 100, 1000]:
            locus = locus_string('chr1', 100, 101, window)
            self.assertNotIn('.', locus, f'non-integral coordinates in {locus}')

    def test_window_clamps_to_start_of_chromosome(self):
        # A window wider than the feature's offset must not run off the left end
        locus = locus_string('chr1', 5, 6, 1000)
        _, start, _ = parse_locus(locus)
        self.assertGreaterEqual(int(start), 1, f'start before position 1 in {locus}')

    def test_window_pads_the_feature_on_both_sides(self):
        # The documented default: a 41bp window on a single base variant
        self.assertEqual('chr1:81-121', locus_string('chr1', 100, 101, 41))

    def test_window_accepts_a_string(self):
        # argparse hands --window through as a string
        self.assertEqual('chr1:81-121', locus_string('chr1', 100, 101, '41'))


class CreateLocusDictTest(unittest.TestCase):
    '''
    create_locus_dict builds the locus for each row of a --no-embed report.  It must agree
    with create_session_dict, which builds the same locus for the embedded report.
    '''

    def single_feature_table(self, feature):
        return types.SimpleNamespace(features=[(feature, 0)])

    def test_agrees_with_session_locus_for_an_snv(self):
        # locus_string does the 0-based to 1-based conversion itself, so both callers pass
        # raw feature coordinates.  A --no-embed report must show the same locus as an
        # embedded one for the same feature.
        feature = Feature('chr1', 100, 101, '')
        locus_dict = create_locus_dict(self.single_feature_table(feature), None)
        self.assertEqual(locus_string('chr1', 100, 101, None), locus_dict['0'])

    def test_agrees_with_session_locus_for_a_range(self):
        # The same agreement on a multi-base feature
        feature = Feature('chr1', 100, 200, '')
        locus_dict = create_locus_dict(self.single_feature_table(feature), None)
        self.assertEqual(locus_string('chr1', 100, 200, None), locus_dict['0'])

    def test_snv_locus_is_not_inverted(self):
        # A 1bp feature must reach the `(end - start) == 1` collapse in locus_string.  A second
        # increment at the call site pushed it past that test and emitted a backwards range.
        feature = Feature('chr1', 100, 101, '')
        locus_dict = create_locus_dict(self.single_feature_table(feature), None)
        _, start, end = parse_locus(locus_dict['0'])
        self.assertLessEqual(int(start), int(end), f'inverted locus {locus_dict["0"]}')

    def test_both_loci_of_a_bedpe_feature_use_the_same_base(self):
        # Both halves of a bedpe row are built from raw feature coordinates
        feature = Feature('chr1', 100, 200, '', '', 'chr1', 100, 200)
        locus_dict = create_locus_dict(self.single_feature_table(feature), None)
        locus1, locus2 = locus_dict['0'].split(' ')
        self.assertEqual(locus1, locus2)


if __name__ == '__main__':
    unittest.main()
