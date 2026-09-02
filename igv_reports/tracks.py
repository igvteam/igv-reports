from igv_reports import feature

def get_track_json_dict(url):

    name = get_name(url)
    format = feature.infer_format(url)
    type = get_track_type(format)

    trackobj = {
        "name": name,
        "url": url,
        "type": type,
        "format": format
    }

    if type == "alignment":
        trackobj["height"] = 500
    elif type == "mut":
        trackobj["height"] = 50
        trackobj["color"] = "rgb(0,0,150)"

    # To respect --exclude-flags, show all reads which are already filtered by
    # pysam in bam.py. igv.js defaults duplicate and vendorFailed to True.
    if format == "bam" or format == "cram":
        trackobj["filter"] = {"duplicate": False, "vendorFailed": False}
    return trackobj

def get_name(filename):

    # Strip any directory, then any extension.  The extension is looked for in the base name,
    # as a "." can precede the last separator (a dotted host name, a versioned directory).
    idx = max(filename.rfind("/"), filename.rfind("\\"))
    basename = filename[idx + 1:]
    period = basename.rfind(".")
    return basename[:period] if period > 0 else basename


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
        "vcf": "variant",
        "wig": "wig",
        "bedgraph": "wig",
        "maf": "mut"
    }
    return dict[format] if format in dict else None

def is_format_supported(format):
    return get_track_type(format) is not None
