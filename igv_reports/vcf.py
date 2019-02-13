import pysam

def get_data(path, region = None):

    vcf = VcfReader(path)

    return vcf.slice(region)


class VcfReader:

    def __init__(self, path):

        self.file = pysam.VariantFile(path)

    def slice(self, region = None):

        vcf = self.file
        header = vcf.header

        fileString = str(header)

        if region == None:
            records = vcf.fetch()
        else:
            records = vcf.fetch(region['chr'], region['start'], region['end'])

        for rec in records:

            fileString += (str(rec))

        return fileString

