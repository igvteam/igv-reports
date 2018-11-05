
from pysam import VariantFile

def get_header(vcfFile):

    vcf = VariantFile(vcfFile)

    return vcf.header



def get_variants(vcfFile):

    vcf = VariantFile(vcfFile)

    return vcf.fetch()


