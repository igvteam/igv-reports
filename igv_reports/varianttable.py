import io
import json
import pysam
from .feature import Feature

class VariantTable:

    # Always remember the *self* argument
    def __init__(self, vcfFile, info_columns = None, info_columns_prefixes = None, sample_columns = None):

        vcf = pysam.VariantFile(vcfFile)

        self.info_fields =  info_columns or []
        self.info_field_prefixes = info_columns_prefixes or []
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
                if h in variant.info:
                    if h == 'ANN':
                        genes, effects, impacts, transcript, gene_id, aa_alt, nt_alt = decode_ann(variant)
                        obj['GENE'] = genes
                        obj['EFFECTS'] = effects
                        obj['IMPACT'] = impacts
                        obj['TRANSCRIPT'] = transcript
                        obj['GENE_ID'] = gene_id
                        obj['PROTEIN ALTERATION'] = aa_alt
                        obj['DNA ALTERATION'] = nt_alt
                    elif h == 'COSMIC_ID':
                        cid = variant.info[h]
                        if cid is not None:
                            if isinstance(cid, str) :
                                return render_id(cid)
                            elif len(cid) == 1:
                                obj[h] = render_id(cid[0])
                            else:
                                tmp = ''
                                for c in cid:
                                    tmp = tmp + render_id(c) + ','
                                obj[h] = tmp
                    else:
                        obj[h] = render_values(variant.info[h])
                else:
                    obj[h] = ''

            for h in self.info_field_prefixes:
                for field in variant.info:
                    if field.startswith(h):
                        obj[field] = render_values(variant.info[field])

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
    if v is None:
        return ""
    elif isinstance(v, float):
        # ensure that we don't waste space by insignificant digits
        return f'{v:.2g}'
    elif isinstance(v, str):
        str_val = v.replace('"', '')
        
        if str_val.startswith('http://') or str_val.startswith('https://'):
            return create_link(str_val)
    
    return str(v)


def render_values(v):
    if v is None:
        return ""
    
    if isinstance(v, str) or isinstance(v, int) or isinstance(v, float):
        return render_value(v)
    return ','.join(map(render_value, v))


def render_id(v):
    if v.startswith('COSM'):
        return (f'<a href = "https://cancer.sanger.ac.uk/cosmic/mutation/overview?'
                f'id={v[4:]}" target="_blank">{v}</a>')
    return v


def render_ids(v):
    return ','.join(map(render_id, v.split(';')))


def decode_ann(variant):
    """Decode the standardized ANN field to something human readable."""
    annotations = ([variant.info['ANN'].split('|'
                   )] if isinstance(variant.info['ANN'],
                   str) else [e.split('|') for e in variant.info['ANN']])
    genes = []
    effects = []
    impacts = []
    transcripts = []
    gene_ids = []
    aa_alts = []
    nt_alts = []
    for allele in variant.alts:
        for ann in annotations:
            ann_allele, kind, impact, gene, gene_id = ann[:5]
            feature_id = ann[6]
            nt_mod, aa_mod = ann[9:11]

            if allele != ann_allele:
                continue

            full = '|'.join(ann)
            # Keep the most severe effect.
            # Link out to Genecards and show the full record in a tooltip.
            genes.append(gene)
            gene_ids.append(gene_id)
            effects.append(kind.replace('&', '/'))
            impacts.append(impact)
            transcripts.append(feature_id)
            aa_alts.append(aa_mod)
            nt_alts.append(nt_mod)
    return ','.join(genes), ','.join(effects), ','.join(impacts), ','.join(transcripts), ','.join(gene_ids), ','.join(aa_alts), ','.join(nt_alts)

def create_link(url):
    """Create an html link for the given url"""
    return (f'<a href = "{url}" target="_blank">{url}</a>')
