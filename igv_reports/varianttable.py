import json
import pysam
import html
from .feature import Feature


class VariantTable:

    # Always remember the *self* argument
    def __init__(self, vcfFile, info_columns=None, info_columns_prefixes=None, samples=None, sample_columns=None, idlink=None):

        vcf = pysam.VariantFile(vcfFile)

        self.info_fields = info_columns or []
        self.idlink = idlink
        self.sample_fields = sample_columns or []
        self.variants = []
        self.features = []  # Bed-like features

        if info_columns_prefixes is not None:
            for p in info_columns_prefixes:
                for info in vcf.header.info:
                    if info.startswith(p):
                        self.info_fields.append(info)

        if samples is not None:
            self.samples = samples
        else :
            self.samples = []
            for s in vcf.header.samples:
                self.samples.append(s)

        for unique_id, var in enumerate(vcf.fetch()):
            self.variants.append((var, unique_id))
            chr = var.chrom
            start = var.pos - 1
            end = start + 1  # TODO -- handle structure variants and deletions > 1 base
            self.features.append((Feature(chr, start, end, ''), unique_id))

    def to_JSON(self):

        json_array = [];

        for variant, unique_id in self.variants:

            escaped_alts = []
            for alt in variant.alts:
                escaped_alts.append(html.escape(alt))

            obj = {
                'unique_id': unique_id,
                'CHROM': variant.chrom,
                'POSITION': variant.pos,
                'REF': html.escape(variant.ref),
                'ALT': ','.join(escaped_alts),
                'ID': ''
            }

            if variant.id is not None:
                obj['ID'] = render_ids(variant.id, self.idlink)

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
                            if isinstance(cid, str):
                                return render_id([cid, self.idlink])
                            elif len(cid) == 1:
                                obj[h] = render_id([cid[0], self.idlink])
                            else:
                                tmp = ''
                                for c in cid:
                                    tmp = tmp + render_id([c, self.idlink]) + ','
                                obj[h] = tmp
                    else:
                        obj[h] = render_values(variant.info[h])
                else:
                    obj[h] = ''

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

        if not any('ID' in obj for obj in json_array):
            # Remove ID column if none of the records actually had an ID.
            for obj in json_array:
                del obj['ID']

        normalized_json = self.normalize_json(json_array)
        return json.dumps(normalized_json)


    def normalize_json(self, json_array):

        headers = ['unique_id', 'CHROM', 'POSITION', 'REF', 'ALT', 'ID']
        if self.info_fields is not None:
            for h in self.info_fields:
                if h == 'ANN':
                    headers = headers + ['GENE', 'EFFECTS', 'IMPACT', 'TRANSCRIPT', 'GENE_ID', 'PROTEIN ALTERATION',
                                         'DNA ALTERATION']
                else:
                    headers.append(h)

        if self.samples is not None and self.sample_fields is not None:
            for s in self.samples:
                for f in self.sample_fields:
                    h = f'{s}:{f}'
                    headers.append(h)

        rows = []
        for json in json_array:
            r = []
            for h in headers:
                if h in json:
                    r.append(json[h])
                else:
                    r.append("")
            rows.append(r)

        return {
            "headers": headers,
            "rows": rows
        }


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

    return html.escape(str(v))


def render_values(v):
    if v is None:
        return ""

    if isinstance(v, str) or isinstance(v, int) or isinstance(v, float):
        return render_value(v)
    return ','.join(map(render_value, v))


def render_id(t):
    v, idlink = t
    if idlink is not None:
        url = idlink.replace("$$", v)
        return (f'<a href = "{url}" target="_blank">{v}</a>')
    elif v.startswith('COSM'):
        return (f'<a href = "https://cancer.sanger.ac.uk/cosmic/mutation/overview?id={v[4:]}" target="_blank">{v}</a>')
    elif v.startswith('rs'):
        return (f'<a href = "https://www.ncbi.nlm.nih.gov/snp/?term={v}" target="_blank">{v}</a>')
    return v


def render_ids(v, idlink=None):
    return ','.join(map(render_id, [(val, idlink) for val in v.split(';')]))


def decode_ann(variant):
    """
    Decode the standardized ANN field to something human readable. This is somewhat fragile and depends on the
    specifics of the ANNOVAR annotation output
    """
    annotations = ([variant.info['ANN'].split('|')] if isinstance(variant.info['ANN'],str) else [e.split('|') for e in variant.info['ANN']])
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

            genes.append(gene)
            gene_ids.append(gene_id)
            effects.append(kind.replace('&', '/'))
            impacts.append(impact)
            transcripts.append(feature_id)
            aa_alts.append(aa_mod)
            nt_alts.append(nt_mod)
    return '<br>'.join(genes), '<br>'.join(effects), '<br>'.join(impacts), '<br>'.join(transcripts), \
           '<br>'.join(gene_ids), '<br>'.join(aa_alts), '<br>'.join(nt_alts)


def create_link(url):
    """Create an html link for the given url"""
    return (f'<a href = "{url}" target="_blank">{url}</a>')
