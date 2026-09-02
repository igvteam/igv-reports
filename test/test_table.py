import unittest
import pathlib
import json
import os
import tempfile
from igv_reports import varianttable, bedtable, generictable
import types


class TableTest(unittest.TestCase):

    def test_get_header(self):

        vcf_path = str((pathlib.Path(__file__).parent / "data/minigenome/variants.vcf").resolve())
        args = self.mock_args()
        table = varianttable.VariantTable(vcf_path, args)
        self.assertEqual(len(table.variants), 28)

    def test_small_del(self):
        path = str((pathlib.Path(__file__).parent / "../test/data/variants/small_deletion.vcf").resolve())
        args = self.mock_args()
        table = varianttable.VariantTable(path, args)
        self.assertEqual(len(table.variants), 1)

    def test_sv(self):
        path = str((pathlib.Path(__file__).parent / "../test/data/variants/SKBR3_Sniffles_sv.vcf").resolve())
        args = self.mock_args()
        table = varianttable.VariantTable(path,args)
        self.assertEqual(len(table.variants), 12)

    def test_bedtable(self):

        bed_file = str((pathlib.Path(__file__).parent / "data/minigenome/variants.bed").resolve())
        table = bedtable.BedTable(bed_file)
        json = table.to_JSON()
        self.assertEqual(len(table.features), 4)
        self.assertTrue(json)

    def test_bedpetable(self):

        bed_file = str((pathlib.Path(__file__).parent / "data/variants.bedpe").resolve())
        table = bedtable.BedpeTable(bed_file)
        json = table.to_JSON()
        self.assertEqual(len(table.features), 9)
        self.assertTrue(json)


    def test_gfftable(self):

        gff = str((pathlib.Path(__file__).parent / "data/minigenome/annotations.gtf.gz").resolve())
        table = bedtable.BedTable(gff)
        json = table.to_JSON()
        self.assertTrue(len(table.features), 2106)
        self.assertTrue(json)


    def test_maftable(self):

        maf_file = str((pathlib.Path(__file__).parent / "data/maf/tcga_test.maf").resolve())
        table = generictable.GenericTable.from_tabfile(maf_file)

        json = table.to_JSON()
        self.assertEqual(len(table.features), 17)
        self.assertTrue(json)

    def test_maflite(self):

        maf_file = str((pathlib.Path(__file__).parent / "data/maf/test.maflite.tsv").resolve())

        info_columns = ["chr", "start", "end", "ref_allele", "alt_allele", "tumor_barcode"]
        sequence = 1
        start = 2
        end = 3

        table = generictable.GenericTable.from_tabfile(maf_file, info_columns, sequence, start, end)

        json = table.to_JSON()
        self.assertEqual(29, len(table.features))
        self.assertTrue(json)


    def test_annovar(self):

        vcf_file = str((pathlib.Path(__file__).parent / "data/annotated_vcf/test.jannovar.vcf").resolve())

        #ANN=A|synonymous_variant|LOW|EGFR|1956|transcript|NM_001346897.1|Coding|19/26|c.2226G>A|p.(%3D)|2483/184056|2226/3276|742/1092||,A|synonymous_variant|LOW|EGFR|1956|transcript|NM_001346898.1|Coding|20/27|c.2361G>A|p.(%3D)|2618/184056|2361/3411|787/1137||,A|synonymous_variant|LOW|EGFR|1956|transcript|NM_001346899.1|Coding|19/27|c.2226G>A|p.(%3D)|2483/189060|2226/3498|742/1166||,A|synonymous_variant|LOW|EGFR|1956|transcript|NM_001346900.1|Coding|20/28|c.2202G>A|p.(%3D)|2415/98264|2202/3474|734/1158||,A|synonymous_variant|LOW|EGFR|1956|transcript|NM_001346941.1|Coding|14/22|c.1560G>A|p.(%3D)|1817/189060|1560/2832|520/944||,A|synonymous_variant|LOW|EGFR|1956|transcript|NM_005228.4|Coding|20/28|c.2361G>A|p.(%3D)|2618/189060|2361/3633|787/1211||;PROB_ABSENT=6086.16;PROB_ALT=0;PROB_ARTIFACT=3093.24;PROB_VERY_RARE=2789.3;SVLEN=.	DP:AF:OBS:SB	221:0.990543:116V-101V+2S-2N+:.
        args = self.mock_args()

        table = varianttable.VariantTable(vcf_file, args)
        json = table.to_JSON()
        self.assertTrue(json is not None)

    def mock_args(self):
        args = types.SimpleNamespace()
        args.info_columns = ["ANN"]
        args.idlink = None
        args.sample_columns = None
        args.info_columns_prefixes = None
        args.samples = None
        args.maxlen = 10000
        return args

    def test_fusions(self):

        fusions_file = str((pathlib.Path(__file__).parent / "data/fusion/igv.fusion_inspector_web.json").resolve())
        table = generictable.GenericTable.from_fusionjson(fusions_file)
        self.assertTrue(table is not None)

    def test_fusions_with_declared_columns(self):

        # A fusion json may name its own columns rather than relying on the default list
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
            json.dump({"columns": ["Fusion", "Splice Type"],
                       "fusions": [{"Fusion": "A--B", "Splice Type": "INCL_NON_REF_SPLICE"}]}, f)
            path = f.name
        try:
            table = generictable.GenericTable.from_fusionjson(path)
            parsed = json.loads(table.to_JSON())
        finally:
            os.unlink(path)

        self.assertEqual(["unique_id", "Fusion", "Splice Type"], parsed["headers"])
        self.assertEqual([[0, "A--B", "INCL_NON_REF_SPLICE"]], parsed["rows"])


class RenderTest(unittest.TestCase):
    '''
    The render_* functions inline VCF content into the report's HTML.  Every value they
    return is written into the document unparsed, so each one has to be escaped.
    '''

    def test_render_value_escapes_plain_strings(self):
        self.assertEqual('&lt;b&gt;x&lt;/b&gt;', varianttable.render_value('<b>x</b>'))

    def test_render_value_formats_floats(self):
        self.assertEqual('1.2e-05', varianttable.render_value(0.00001234))

    def test_render_value_of_none_is_empty(self):
        self.assertEqual('', varianttable.render_value(None))

    def test_render_values_joins_collections(self):
        self.assertEqual('a,b', varianttable.render_values(('a', 'b')))

    def test_render_id_links_known_id_formats(self):
        self.assertIn('ncbi.nlm.nih.gov/snp', varianttable.render_id(['rs123', None]))
        self.assertIn('cancer.sanger.ac.uk', varianttable.render_id(['COSM123', None]))

    def test_render_ids_splits_on_semicolon(self):
        rendered = varianttable.render_ids('rs123;rs456')
        self.assertEqual(2, len(rendered.split(',')))

    def test_render_id_escapes_html(self):
        # A VCF ID holding markup must not reach the document as markup
        self.assertNotIn('<img', varianttable.render_id(['<img src=x onerror=y>', None]))

    def test_render_id_escapes_html_in_a_linked_id(self):
        # ... on each of the branches that builds a link
        self.assertNotIn('<img', varianttable.render_id(['rs<img src=x onerror=y>', None]))
        self.assertNotIn('<img', varianttable.render_id(['COSM<img src=x onerror=y>', None]))

    def test_render_id_escapes_the_idlink_substitution(self):
        # $$ is replaced with the id, so the id must not break out of the href
        rendered = varianttable.render_id(['" onmouseover="x', 'https://example.org/?t=$$'])
        self.assertNotIn('onmouseover="x', rendered)

    def test_render_value_escapes_inside_links(self):
        # An INFO field beginning with http:// becomes a link; its content is still escaped
        rendered = varianttable.render_value('http://x/<script>a</script>')
        self.assertNotIn('<script>', rendered)

    def test_render_id_link_targets_are_unchanged_for_ordinary_ids(self):
        self.assertEqual(
            '<a href = "https://www.ncbi.nlm.nih.gov/snp/?term=rs123" target="_blank">rs123</a>',
            varianttable.render_id(['rs123', None]))


class CosmicIdTest(unittest.TestCase):

    def mock_args(self, info_columns):
        args = types.SimpleNamespace()
        args.info_columns = info_columns
        args.idlink = None
        args.sample_columns = None
        args.info_columns_prefixes = None
        args.samples = None
        args.maxlen = 10000
        return args

    def test_multivalued_cosmic_id(self):
        # COSMIC_ID declared Number=. -- pysam yields a tuple, which takes the working branch
        path = str((pathlib.Path(__file__).parent / "data/variants/variants.vcf").resolve())
        table = varianttable.VariantTable(path, self.mock_args(["COSMIC_ID"]))
        parsed = json.loads(table.to_JSON())
        self.assertIn('COSMIC_ID', parsed["headers"])

    def test_scalar_cosmic_id(self):
        # COSMIC_ID declared Number=1 -- pysam yields a str, which must be assigned to the
        # column like every other branch rather than returned from to_JSON
        path = str((pathlib.Path(__file__).parent / "data/variants/cosmic_scalar.vcf").resolve())
        table = varianttable.VariantTable(path, self.mock_args(["COSMIC_ID"]))
        rendered = table.to_JSON()
        try:
            parsed = json.loads(rendered)
        except ValueError:
            self.fail(f'to_JSON did not return JSON: {rendered[:80]!r}')
        self.assertEqual(2, len(parsed["rows"]))
