import io
import json
import pysam
from .feature import Feature

class VariantTable:

    # Always remember the *self* argument
    def __init__(self, vcfFile, infoColumns=None):

        vcf = pysam.VariantFile(vcfFile)

        self.infoFields =  infoColumns if infoColumns else []
        self.variants = []
        self.features = []   #Bed-like features

        for unique_id, var in enumerate(vcf.fetch()):
            self.variants.append((var, unique_id))
            chr = var.chrom
            start = var.pos - 1
            end = start + 1       #TODO -- handle structure variants and deletions > 1 base
            self.features.append((Feature(chr, start, end, ''), unique_id))

    def to_JSON(self):


        jsonArray = [];

        for variant, unique_id in self.variants:
            obj = {
                "unique_id": unique_id,
                "CHROM": variant.chrom,
                "POSITION": variant.pos,
                "REF": variant.ref,
                "ALT": ','.join(variant.alts),
            }

            for h in self.infoFields:
                v = ''
                if h in variant.info:
                    v = variant.info[h]
                    if not isinstance(v, str):
                        v = ','.join(map(str, v))

                if h == "COSMIC_ID":
                    v = '<a href = "https://cancer.sanger.ac.uk/cosmic/mutation/overview?id={id}" target="_blank">{v}</a>'.format(v=v, id=v[4:])

                obj[h] = v

            jsonArray.append(obj)

        return json.dumps(jsonArray)




