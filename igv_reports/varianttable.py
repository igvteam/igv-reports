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

        unique_id = 1
        for var in vcf.fetch():
            self.variants.append((var, unique_id))
            chr = var.chrom
            start = var.pos - 1
            end = start + 1       #TODO -- handle structure variants and deletions > 1 base
            self.features.append((Feature(chr, start, end, ''), unique_id))
            unique_id += 1

    def to_JSON(self):


        jsonArray = [];

        for tuple in self.variants:

            variant = tuple[0]
            unique_id = tuple[1]
            obj = dict()
            obj["unique_id"] = unique_id
            obj["CHROM"] = variant.chrom
            obj["POSITION"] = variant.pos
            obj["REF"] = variant.ref
            obj["ALT"] = ','.join(variant.alts)

            for h in self.infoFields:

                keys = set(variant.info.keys())

                if h in keys:
                    v = ""
                    tuples = variant.info[h]
                    for e in tuples:
                        if(v):
                            v = v + ","
                        v = v + str(e)
                else:
                    v = ''

                if h == "COSMIC_ID":
                    v = '<a href = "https://cancer.sanger.ac.uk/cosmic/mutation/overview?id=4006021" target="_blank">' + v + '</a>'

                obj[h] = v

            jsonArray.append(obj)

        return json.dumps(jsonArray)




