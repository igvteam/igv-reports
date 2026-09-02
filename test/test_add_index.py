import unittest
from unittest import mock

from igv_reports.report import add_index


def only(*existing):
    """A resource_exists stub that reports just the given urls as present."""
    return lambda url: url in existing


class AddIndexTest(unittest.TestCase):
    '''
    add_index attaches an index url to a --no-embed track config by probing for the
    conventional index names.  Every probe must be built from the track url.
    '''

    def add_index(self, config, *existing):
        with mock.patch('igv_reports.report.resource_exists', side_effect=only(*existing)):
            add_index(config)
        return config

    def test_bam_bai(self):
        config = self.add_index({"url": "http://host/x.bam", "format": "bam"},
                                "http://host/x.bam.bai")
        self.assertEqual("http://host/x.bam.bai", config["indexURL"])

    def test_bam_csi(self):
        config = self.add_index({"url": "http://host/x.bam", "format": "bam"},
                                "http://host/x.bam.csi")
        self.assertEqual("http://host/x.bam.csi", config["indexURL"])

    def test_bam_bai_replacing_the_extension(self):
        # Some pipelines name the index x.bai rather than x.bam.bai
        config = self.add_index({"url": "http://host/x.bam", "format": "bam"},
                                "http://host/x.bai")
        self.assertEqual("http://host/x.bai", config["indexURL"])

    def test_cram_crai(self):
        config = self.add_index({"url": "http://host/x.cram", "format": "cram"},
                                "http://host/x.cram.crai")
        self.assertEqual("http://host/x.cram.crai", config["indexURL"])

    def test_tabix_tbi(self):
        config = self.add_index({"url": "http://host/x.vcf.gz", "format": "vcf"},
                                "http://host/x.vcf.gz.tbi")
        self.assertEqual("http://host/x.vcf.gz.tbi", config["indexURL"])

    def test_tabix_csi(self):
        config = self.add_index({"url": "http://host/x.vcf.gz", "format": "vcf"},
                                "http://host/x.vcf.gz.csi")
        self.assertEqual("http://host/x.vcf.gz.csi", config["indexURL"])

    def test_no_index_found(self):
        config = self.add_index({"url": "http://host/x.bam", "format": "bam"})
        self.assertNotIn("indexURL", config)

    def test_existing_index_is_left_alone(self):
        config = self.add_index({"url": "http://host/x.bam", "format": "bam",
                                 "indexURL": "http://host/custom.bai"},
                                "http://host/x.bam.bai")
        self.assertEqual("http://host/custom.bai", config["indexURL"])

    def test_config_without_a_url(self):
        config = self.add_index({"format": "bam"}, "http://host/x.bam.bai")
        self.assertNotIn("indexURL", config)


if __name__ == '__main__':
    unittest.main()
