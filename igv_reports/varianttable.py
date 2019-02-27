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
                    if h == "ANN":
                        v = decode_ann(variant)
                    else:
                        v = variant.info[h]
                        if not isinstance(v, str):
                            v = ','.join(map(str, v))


                if h == "COSMIC_ID":
                    v = '<a href = "https://cancer.sanger.ac.uk/cosmic/mutation/overview?id={id}" target="_blank">{v}</a>'.format(v=v, id=v[4:])

                obj[h] = v

            jsonArray.append(obj)

        return json.dumps(jsonArray)


def decode_ann(variant):
    annotations = [e.split("|") for e in variant.info["ANN"]]
    effects = []
    for allele in variant.alts:
        for ann in annotations:
            ann_allele, kind, impact, gene = ann[:4]
            aa_mod = ann[10]
            if aa_mod:
                # add separator if present
                aa_mod = ':{aa_mod}'

            if allele != ann_allele:
                continue

            full = "|".join(ann)
            # keep the most severe effect
            effects.append(f'<a href="https://www.genecards.org/Search/Keyword?'
                           f'queryString={gene}" target="_blank">{gene}</a>:<abbr title="{full}">'
                           f'{kind}{aa_mod}</abbr>')
            break
    return ",".join(effects)
