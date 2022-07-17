import json
import html
from .feature import parse


class BedTable:

    # Always remember the *self* argument
    def __init__(self, bed_file, split_bool=False):

        self.features = []

        featureList = parse(bed_file, split_bool=split_bool)
        unique_id = 0
        for var in featureList:
            self.features.append((var, unique_id))
            unique_id += 1

    def to_JSON(self):

        # Test whether data is single locus or multi locus without accessing
        # the split_bool variable. to_JSON() is a generic function present
        # in multiple classes and we do not want to change their definitions.
        # Since features should already have chr2/start2/end2, we can look
        # them up and see if we have two locations.
        if (self.features[0][0]).chr2 == '' and (self.features[0][0]).start2 == 0:
            headers = ["unique_id", "Chrom", "Start", "End", "Name"]
            rows = []

            for tuple in self.features:
                feature = tuple[0]
                unique_id = tuple[1]
                rows.append([unique_id, feature.chr, feature.start+1, feature.end, html.escape(feature.name)])
        else:
            headers = ["unique_id", "Chrom_A", "Start_A", "End_A", "Chrom_B", "Start_B", "End_B", "Name"]
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
        session_dict = {}
        for f in featureList:
            #expand name field
            name_tokens = f.name.split(";")
            for token in name_tokens:
                kv = token.split("=")
                key = kv[0]
                value = kv[1]
                setattr(f, key, value)

            #create new session ID?
            if hasattr(f, 'viewport'):
                self.features.append((f, unique_id))
                unique_id += 1
                viewport = f.viewport
                if viewport in session_dict:
                    sid = session_dict[viewport]
                else:
                    sid = str(session_id)
                    session_dict[viewport] = sid
                    session_id = session_id + 1
                f.session_id = sid

    def to_JSON(self):

        json_array = [];

        for tuple in self.features:

            feature = tuple[0]
            name_tokens = feature.name.split(";")
            if hasattr(feature, 'session_id'):
                unique_id = tuple[1]
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
                        kv = token.split("=")
                        key = kv[0]
                        if key != 'viewport':
                            value = kv[1]
                            obj[key] = value
                else:
                    dict = {}
                    for token in name_tokens:
                        kv = token.split("=")
                        dict[kv[0]] = kv[1]
                    for key in self.table_columns:
                        if key in dict:
                            obj[key] = dict[key]
                        else:
                            obj[key] = ''


                json_array.append(obj)

        normalized = normalize_json(self.table_columns, json_array)
        return json.dumps(normalized)


def normalize_json(info_fields, json_array):

    headers = ['unique_id', 'CHROM', 'POSITION', 'REF', 'ALT', 'ID']
    if info_fields is not None:
        for h in info_fields:
            if h == 'ANN':
                headers = headers + [ 'GENE', 'EFFECTS', 'IMPACT', 'TRANSCRIPT', 'GENE_ID', 'PROTEIN ALTERATION', 'DNA ALTERATION']
            else:
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
