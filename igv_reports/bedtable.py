import json
import html
from .feature import parse


class BedTable:

    # Always remember the *self* argument
    def __init__(self, bed_file):

        self.features = []

        featureList = parse(bed_file)
        unique_id = 0
        self.has_name = False
        for feature in featureList:
            if len(feature.name) > 0:
                self.has_name = True
            self.features.append((feature, unique_id))
            unique_id += 1

    def to_JSON(self):

        headers = ["unique_id", "Chrom", "Start", "End"]
        if self.has_name:
            headers.append("Name")
        rows = []

        for tuple in self.features:
            feature = tuple[0]
            unique_id = tuple[1]
            rows.append([unique_id, feature.chr, feature.start+1, feature.end, html.escape(feature.name)])

        return json.dumps({
            "headers": headers,
            "rows": rows
        })

class BedpeTable:

    # Always remember the *self* argument
    def __init__(self, bedpe_file):

        self.features = []

        featureList = parse(bedpe_file)
        unique_id = 0
        self.has_name = False
        for feature in featureList:
            if len(feature.name) > 0:
                self.has_name = True
            self.features.append((feature, unique_id))
            unique_id += 1

    def to_JSON(self):

        headers = ["unique_id", "Chrom_A", "Start_A", "End_A", "Chrom_B", "Start_B", "End_B"]
        if self.has_name:
            headers.append("Name")
        rows = []

        for tuple in self.features:
            feature = tuple[0]
            unique_id = tuple[1]
            rows.append([unique_id, feature.chr, feature.start+1, feature.end, feature.chr2, feature.start2+1, feature.end2, html.escape(feature.name)])

        return json.dumps({
            "headers": headers,
            "rows": rows
        })


class JunctionBedTable:

    # Always remember the *self* argument
    def __init__(self, bed_file, info_columns = None):

        self.features = []
        self.table_columns =  info_columns or None
        featureList = parse(bed_file)
        unique_id = 1
        session_id = 1
        viewport_to_session_id = {}
        for f in featureList:
            #expand name field
            name_tokens = f.name.split(";")
            for token in name_tokens:
                # Ignore name tokens that are not key=value pairs, e.g. a plain bed feature name
                key, sep, value = token.partition("=")
                if sep:
                    setattr(f, key, value)

            # Junction report variants are defined in rows with "viewport" attributes.  Its possible multiple variants
            # share the same viewport, if this is the case they can share a session. This is a space optimization.
            if hasattr(f, 'viewport'):
                self.features.append((f, unique_id))
                unique_id += 1
                viewport = f.viewport
                if viewport in viewport_to_session_id:
                    sid = viewport_to_session_id[viewport]
                else:
                    sid = str(session_id)
                    viewport_to_session_id[viewport] = sid
                    session_id += 1
                f.session_id = sid

    def to_JSON(self):

        json_array = [];
        id_to_session = {}
        for tuple in self.features:

            feature = tuple[0]
            name_tokens = feature.name.split(";")
            unique_id = tuple[1]
            id_to_session[unique_id] = feature.session_id
            obj = {
                "unique_id": unique_id,
                "session_id": feature.session_id,
                "viewport": feature.viewport,
                "feature_locus": feature.chr + ":" + str(feature.start) + "-" + str(feature.end),
                "Chrom": feature.chr,
                "Start": feature.start + 1,
                "End": feature.end
            }

            if self.table_columns == None:
                for token in name_tokens:
                    key, sep, value = token.partition("=")
                    if sep and key != 'viewport':
                        obj[key] = value
            else:
                dict = {}
                for token in name_tokens:
                    key, sep, value = token.partition("=")
                    if sep:
                        dict[key] = value
                for key in self.table_columns:
                    if key in dict:
                        obj[key] = dict[key]
                    else:
                        obj[key] = ''


            json_array.append(obj)

        normalized = normalize_json(self.table_columns, json_array)
        normalized["id_to_session"] = id_to_session
        return json.dumps(normalized)


# Junction table fields used to drive the viewer, not to be displayed as table columns
JUNCTION_INTERNAL_FIELDS = ('session_id', 'viewport', 'feature_locus')


def normalize_json(info_fields, json_array):

    headers = ['unique_id', 'Chrom', 'Start', 'End']
    if info_fields is not None:
        headers = headers + list(info_fields)
    else:
        # Columns are whatever attributes the bed name field defined, in first seen order
        for obj in json_array:
            for h in obj:
                if h not in headers and h not in JUNCTION_INTERNAL_FIELDS:
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
