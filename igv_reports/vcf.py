import pysam

def get_data(path, region = None):

    vcf = VcfReader(path)

    return vcf.slice(region)


class VcfReader:

    def __init__(self, path):

        self.file = pysam.VariantFile(path)

    def slice(self, region = None, region2=None, split_bool=False):

        vcf = self.file
        header = vcf.header

        fileString = str(header)

        if region == None:
            records = vcf.fetch()
        else:
            records = vcf.fetch(region['chr'], region['start'], region['end'])

        for rec in records:

            fileString += (str(rec))

        if not split_bool:
            return fileString
        else:
            records2 = vcf.fetch(region2['chr'], region2['start'], region2['end'])
            for rec in records2:
                fileString += (str(rec))
            return fileString
