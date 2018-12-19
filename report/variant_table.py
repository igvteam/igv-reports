import io
import json

from pysam import VariantFile


class VariantTable:

    # Always remember the *self* argument
    def __init__(self, vcfFile, headerFile):

        vcf = VariantFile(vcfFile)

        self.infoFields = []
        if headerFile:
            self.infoFields = headerFile.split(",")

        self.variants = []
        unique_id = 1
        for var in vcf.fetch():
            self.variants.append((var, unique_id))
            unique_id += 1

    def to_JSON(self):

        out = io.StringIO()

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
                    v = ','.join(str(variant.info[h]))
                else:
                    v = ''

                if h == "COSMIC_ID":
                    v = '<a href = "https://cancer.sanger.ac.uk/cosmic/mutation/overview?id=4006021" target="_blank">' + v + '</a>'

                obj[h] = v

            jsonArray.append(obj)

        json.dump(jsonArray, out)

        return out.getvalue();


