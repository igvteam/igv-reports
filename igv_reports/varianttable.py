import io
import json
import pysam
from .feature import Feature

class VariantTable:

    # Always remember the *self* argument
    def __init__(self, vcfFile, info_columns = None, sample_columns = None):

        vcf = pysam.VariantFile(vcfFile)

        self.info_fields =  info_columns or []
        self.sample_fields = sample_columns or []
        self.variants = []
        self.features = []   #Bed-like features

        for unique_id, var in enumerate(vcf.fetch()):
            self.variants.append((var, unique_id))
            chr = var.chrom
            start = var.pos - 1
            end = start + 1       #TODO -- handle structure variants and deletions > 1 base
            self.features.append((Feature(chr, start, end, ''), unique_id))

    def to_JSON(self):


        json_array = [];

        for variant, unique_id in self.variants:
            obj = {
                'unique_id': unique_id,
                'CHROM': variant.chrom,
                'POSITION': variant.pos,
                'REF': variant.ref,
                'ALT': ','.join(variant.alts),
                'ID': ''
            }

            if variant.id is not None:
                obj['ID'] = render_ids(variant.id)

            for h in self.info_fields:
                v = ''
                if h in variant.info:
                    if h == 'ANN':
                        v = decode_ann(variant)
                    elif h == 'COSMIC_ID':
                        v = render_id(v)
                    else:
                        v = render_values(variant.info[h])

                obj[h] = v

            for h in self.sample_fields:
                for sample, values in variant.samples.items():
                    v = ''
                    try:
                        v = values[h]
                    except KeyError:
                        # ignore if key is not present
                        pass

                    obj[f'{sample}:{h}'] = render_values(v)

            json_array.append(obj)

        if not any(obj['ID'] for obj in json_array):
            # Remove ID column if none of the records actually had an ID.
            for obj in json_array:
                del obj['ID']
        return json.dumps(json_array)


def render_value(v):
    """Render given value to string."""
    if isinstance(v, float):
        # ensure that we don't waste space by insignificant digits
        return f'{v:.2g}'
    return str(v)


def render_values(v):
    if not isinstance(v, str):
        return ','.join(map(render_value, v))
    return v


def render_id(v):
    if v.startswith('COSM'):
        return (f'<a href = "https://cancer.sanger.ac.uk/cosmic/mutation/overview?'
                f'id={v[4:]}" target="_blank">{v}</a>')
    return v


def render_ids(v):
    return ','.join(map(render_id, v.split(';')))


def decode_ann(variant):
    """Decode the standardized ANN field to something human readable."""
    annotations = [e.split("|") for e in variant.info["ANN"]]
    effects = []
    for allele in variant.alts:
        for ann in annotations:
            ann_allele, kind, impact, gene = ann[:4]
            aa_mod = ann[10]
            if aa_mod:
                # add separator if present
                aa_mod = f':{aa_mod}'

            if allele != ann_allele:
                continue

            full = '|'.join(ann)
            # Keep the most severe effect.
            # Link out to Genecards and show the full record in a tooltip.
            effects.append(f'<a href="https://www.genecards.org/cgi-bin/carddisp.pl?'
                           f'gene={gene}" target="_blank">{gene}</a>:<abbr title="{full}">'
                           f'{kind}{aa_mod}</abbr>')
            break
    return ','.join(effects)
