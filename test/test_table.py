import unittest
import pathlib
from igv_reports import varianttable, bedtable, generictable

class TableTest(unittest.TestCase):

    def test_get_header(self):

        vcf_path = str((pathlib.Path(__file__).parent / "data/minigenome/variants.vcf").resolve())
        table = varianttable.VariantTable(vcf_path)
        self.assertEqual(len(table.variants), 28)

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
        table = generictable.GenericTable(maf_file)

        json = table.to_JSON()
        self.assertEqual(len(table.features), 17)
        self.assertTrue(json)

    def test_maflite(self):

        maf_file = str((pathlib.Path(__file__).parent / "data/maf/test.maflite.tsv").resolve())

        info_columns = ["chr", "start", "end", "ref_allele", "alt_allele", "tumor_barcode"]
        sequence = 1
        start = 2
        end = 3

        table = generictable.GenericTable(maf_file, info_columns, sequence, start, end)

        json = table.to_JSON()
        self.assertEqual(29, len(table.features))
        self.assertTrue(json)


    def test_annovar(self):

        vcf_file = str((pathlib.Path(__file__).parent / "data/annotated_vcf/test.jannovar.vcf").resolve())

        #ANN=A|synonymous_variant|LOW|EGFR|1956|transcript|NM_001346897.1|Coding|19/26|c.2226G>A|p.(%3D)|2483/184056|2226/3276|742/1092||,A|synonymous_variant|LOW|EGFR|1956|transcript|NM_001346898.1|Coding|20/27|c.2361G>A|p.(%3D)|2618/184056|2361/3411|787/1137||,A|synonymous_variant|LOW|EGFR|1956|transcript|NM_001346899.1|Coding|19/27|c.2226G>A|p.(%3D)|2483/189060|2226/3498|742/1166||,A|synonymous_variant|LOW|EGFR|1956|transcript|NM_001346900.1|Coding|20/28|c.2202G>A|p.(%3D)|2415/98264|2202/3474|734/1158||,A|synonymous_variant|LOW|EGFR|1956|transcript|NM_001346941.1|Coding|14/22|c.1560G>A|p.(%3D)|1817/189060|1560/2832|520/944||,A|synonymous_variant|LOW|EGFR|1956|transcript|NM_005228.4|Coding|20/28|c.2361G>A|p.(%3D)|2618/189060|2361/3633|787/1211||;PROB_ABSENT=6086.16;PROB_ALT=0;PROB_ARTIFACT=3093.24;PROB_VERY_RARE=2789.3;SVLEN=.	DP:AF:OBS:SB	221:0.990543:116V-101V+2S-2N+:.

        table = varianttable.VariantTable(vcf_file, info_columns=["ANN"])
        json = table.to_JSON()
        self.assertTrue(json is not None)



