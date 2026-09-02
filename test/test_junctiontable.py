import json
import pathlib
import tempfile
import unittest

from igv_reports.bedtable import JunctionBedTable


class JunctionBedTableTest(unittest.TestCase):
    '''
    Junction rows carry their attributes as key=value pairs in the bed name field.  The table
    columns are those attributes, not the variant table's CHROM/POSITION/REF/ALT/ID.
    '''

    def setUp(self):
        self.bed = str((pathlib.Path(__file__).parent / "data/junctions/Introns.38.bed").resolve())

    def to_json(self, table):
        return json.loads(table.to_JSON())

    def test_columns_are_the_name_field_attributes(self):

        parsed = self.to_json(JunctionBedTable(self.bed))
        self.assertEqual(
            ['unique_id', 'Chrom', 'Start', 'End',
             'uniquely_mapped', 'multi_mapped', 'gene', 'TCGA', 'GTEx', 'variant_name'],
            parsed["headers"])

    def test_rows_are_populated(self):

        parsed = self.to_json(JunctionBedTable(self.bed))
        self.assertEqual(4, len(parsed["rows"]))
        for row in parsed["rows"]:
            self.assertEqual(len(parsed["headers"]), len(row))
            # No row is entirely blank past the id
            self.assertTrue(any(cell != '' for cell in row[1:]))

    def test_locus_columns_carry_the_feature_coordinates(self):

        parsed = self.to_json(JunctionBedTable(self.bed))
        first = dict(zip(parsed["headers"], parsed["rows"][0]))
        self.assertEqual('chr7', first['Chrom'])
        self.assertEqual(55200414, first['Start'])   # 1-based
        self.assertEqual(55202516, first['End'])
        self.assertEqual('EGFRvIVb', first['variant_name'])

    def test_info_columns_select_the_displayed_attributes(self):

        parsed = self.to_json(JunctionBedTable(self.bed, ["TCGA", "GTEx", "variant_name"]))
        self.assertEqual(['unique_id', 'Chrom', 'Start', 'End', 'TCGA', 'GTEx', 'variant_name'],
                         parsed["headers"])

    def test_internal_fields_are_not_columns(self):

        parsed = self.to_json(JunctionBedTable(self.bed))
        for field in ['session_id', 'viewport', 'feature_locus']:
            self.assertNotIn(field, parsed["headers"])

    def test_rows_sharing_a_viewport_share_a_session(self):

        parsed = self.to_json(JunctionBedTable(self.bed))
        # Three rows use the EGFR viewport, one uses the MET viewport
        self.assertEqual({'1': '1', '2': '1', '3': '2', '4': '1'}, parsed["id_to_session"])

    def test_plain_name_field_is_skipped(self):

        # A bed name that is not a key=value list must not abort the report
        with tempfile.NamedTemporaryFile('w', suffix='.bed', delete=False) as f:
            f.write("chr7\t100\t200\tEGFR\t10\t+\n")
            f.write("chr7\t300\t400\tgene=EGFR;viewport=chr7:1-1000\t10\t+\n")
            path = f.name
        self.addCleanup(pathlib.Path(path).unlink)

        parsed = self.to_json(JunctionBedTable(path))
        # Only the row defining a viewport becomes a junction row
        self.assertEqual(1, len(parsed["rows"]))
        self.assertEqual(['unique_id', 'Chrom', 'Start', 'End', 'gene'], parsed["headers"])


if __name__ == '__main__':
    unittest.main()
