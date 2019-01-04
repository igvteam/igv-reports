import unittest

from igv_reports.variant_table import VariantTable

class TableTest(unittest.TestCase):

    def test_get_header(self):

        table = VariantTable('data/mut1/cancer.vcf.gz', '/Users/jrobinso/igv-team Dropbox/James Robinson/projects/igv.js-reports/example/MI_viewer/info_columns.txt')

        self.assertTrue(table)

        print(table.to_JSON())

