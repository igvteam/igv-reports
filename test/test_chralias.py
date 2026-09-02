import unittest

from igv_reports.chr_alias import get_chromosome_alias
from igv_reports.chralias import build_aliastable, get_alias


class ChrAliasTest(unittest.TestCase):
    '''
    Two implementations of the same concept.  get_alias (chralias.py) backs the alias tables
    of FeatureReader and IdeogramReader; get_chromosome_alias (chr_alias.py) backs FastaReader
    and TwoBitReader.  They must agree, or a chromosome name resolves in one track and not another.
    '''

    def test_get_alias_adds_and_strips_prefix(self):
        self.assertEqual('1', get_alias('chr1'))
        self.assertEqual('chr1', get_alias('1'))
        self.assertEqual('X', get_alias('chrX'))
        self.assertEqual('chrX', get_alias('X'))

    def test_get_chromosome_alias_adds_and_strips_prefix(self):
        self.assertEqual('1', get_chromosome_alias('chr1'))
        self.assertEqual('chr1', get_chromosome_alias('1'))

    def test_get_chromosome_alias_handles_mitochondria(self):
        self.assertEqual('MT', get_chromosome_alias('chrM'))
        self.assertEqual('chrM', get_chromosome_alias('MT'))

    def test_build_aliastable_handles_mitochondria(self):
        # build_aliastable gets chrM right, which is why the fasta/bam/wig paths work
        self.assertEqual({'MT': 'chrM', '1': 'chr1'}, build_aliastable(['chrM', 'chr1']))

    def test_alias_of_an_alias_round_trips(self):
        for name in ['chr1', '1', 'chrX', 'X']:
            self.assertEqual(name, get_alias(get_alias(name)))

    @unittest.expectedFailure
    def test_get_alias_handles_mitochondria(self):
        # BUG chralias.py:26-31 -- returns the input unchanged for both mitochondrial spellings.
        # Observed: get_alias('chrM') == 'chrM', get_alias('MT') == 'MT'.  FeatureReader keys its
        # alias table with get_alias(f.chr) (feature.py:126), so an 'MT' query against a file
        # using 'chrM' silently returns no features.
        self.assertEqual('MT', get_alias('chrM'))
        self.assertEqual('chrM', get_alias('MT'))

    @unittest.expectedFailure
    def test_the_two_implementations_agree(self):
        for name in ['chr1', '1', 'chrX', 'X', 'chrM', 'MT']:
            self.assertEqual(get_chromosome_alias(name), get_alias(name), f'disagreement on {name}')


if __name__ == '__main__':
    unittest.main()
