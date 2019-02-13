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
