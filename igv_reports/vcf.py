import pysam

def get_data(vcfFile, region = None):

    vcf = pysam.VariantFile(vcfFile)

    header = vcf.header

    fileString = str(header)

    if region == None:
        records = vcf.fetch()
    else:
        records = vcf.fetch(region['chr'], region['start'], region['end'])

    for rec in records:

        fileString += (str(rec))

    return fileString
