import json

from .feature import parse


class BedTable:

    # Always remember the *self* argument
    def __init__(self, bed_file):

        self.features = []

        featureList = parse(bed_file)
        unique_id = 1
        for var in featureList:
            self.features.append((var, unique_id))
            unique_id += 1

    def to_JSON(self):

        jsonArray = [];

        for tuple in self.features:
            feature = tuple[0]
            unique_id = tuple[1]
            obj = {
                "unique_id": unique_id,
                "Chrom": feature.chr,
                "Start": feature.start + 1,
                "End": feature.end,
                "Name": feature.name
            }

            jsonArray.append(obj)

        return json.dumps(jsonArray)



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

        jsonArray = [];

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


                jsonArray.append(obj)

        return json.dumps(jsonArray)
