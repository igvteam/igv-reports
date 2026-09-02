import unittest

from igv_reports.feature import infer_format


class InferFormatTest(unittest.TestCase):

    def test_known_extensions(self):
        self.assertEqual('bam', infer_format('/data/x.bam'))
        self.assertEqual('vcf', infer_format('/data/x.vcf'))
        self.assertEqual('bed', infer_format('/data/x.bed'))
        self.assertEqual('bedpe', infer_format('/data/x.bedpe'))
        self.assertEqual('gff', infer_format('/data/x.gff3'))
        self.assertEqual('wig', infer_format('/data/x.wig'))

    def test_gzipped_extension(self):
        self.assertEqual('vcf', infer_format('x.vcf.gz'))
        self.assertEqual('bed', infer_format('/data/x.bed.gz'))

    def test_case_is_ignored(self):
        self.assertEqual('vcf', infer_format('/data/X.VCF'))

    def test_unknown_extension_falls_through(self):
        self.assertEqual('unknown', infer_format('file.unknown'))
        self.assertIsNone(infer_format('noextension'))

    def test_url_query_string_is_not_part_of_the_extension(self):
        # A presigned url carries its signature in the query string
        self.assertEqual('vcf', infer_format('http://host/x.vcf?a=1'))
        self.assertEqual('bam', infer_format('https://host/x.bam?X-Amz-Signature=abc'))
        self.assertEqual('vcf', infer_format('https://host/x.vcf.gz?a=1'))

    def test_url_fragment_is_not_part_of_the_extension(self):
        self.assertEqual('bed', infer_format('http://host/a.bed#frag'))

    def test_question_mark_in_a_local_path_is_preserved(self):
        # Only urls are stripped -- '?' is a legal character in a local file name
        self.assertEqual('bed', infer_format('/data/odd?name.bed'))

    def test_refgene_names_the_file_not_the_directory(self):
        self.assertEqual('refgene', infer_format('/data/refGene.txt'))
        self.assertEqual('refgene', infer_format('http://host/refseq.txt'))
        # A directory called refgene must not make every file in it a refgene file
        self.assertEqual('txt', infer_format('/refgene_dir/x.txt'))

    def test_recognized_extension_wins_over_refgene(self):
        self.assertEqual('bed', infer_format('/data/refGene.bed'))


if __name__ == '__main__':
    unittest.main()
