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

    return trackobj

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
        "vcf": "variant",
        "wig": "wig",
        "bedgraph": "wig",
        "maf": "mut"
    }
    return dict[format]
