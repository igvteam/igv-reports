import os


def infer_format(filename):

    filename = filename.lower()
    if(filename.endswith(".gz")):
        filename = filename[:-3]

    if filename.endswith(".bam"):
        return "bam"
    if filename.endswith(".cram"):
        return "cram"
    elif filename.endswith(".vcf"):
        return "vcf"
    elif filename.endswith(".bed"):
        return "bed"
    elif filename.endswith(".gff") or filename.endswith(".gff3"):
        return "gff3"
    elif filename.endswith(".gtf"):
        return "gtf"

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
        "vcf": "variant"
    }
    return dict[format]

def get_track_json_dict(filename):

    name = get_name(filename)
    format = infer_format(filename)
    type = get_track_type(format)
    return {
        "name": name,
        "type": type,
        "format": format
    }

def istabix(filename):

    return filename.endswith(".gz") and os.path.exists(filename + ".tbi")