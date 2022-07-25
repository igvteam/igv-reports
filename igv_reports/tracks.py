from igv_reports import feature

def get_track_json_dict(filename):

    name = get_name(filename)
    format = feature.infer_format(filename)
    # Note: CRAM files are output in BAM format
    if format == 'cram':
        format = 'bam'
    # Note: BCF files are output in VCF format
    if format == 'bcf':
        format = 'vcf'
    type = get_track_type(format)
    return {
        "name": name,
        "url": filename,
        "type": type,
        "format": format
    }

def get_name(filename):

    idx = filename.rfind("/")
    if idx < 0:
        idx = filename.rfind("\\")
    period = filename.rfind(".")
    if idx < 0:
        if period < 0:
            return filename
        else:
            return filename[:period]
    else:
        idx += 1
        if period < 0:
            return filename[idx]
        else:
            return filename[idx:period]


def get_track_type(format):

    dict = {
        "bam": "alignment",
        "cram": "alignment",
        "bed": "annotation",
        "gff3": "annotation",
        "gff": "annotation",
        "gtf": "annotation",
        "bed": "annotation",
        "refgene": "annotation",
        "bcf": "variant",
        "vcf": "variant"
    }
    return dict[format]
