import json
import sys
import html
from .feature import parse

class GenericTable:

    def __init__(self, file, info_columns = None, sequence = None, begin = None, end = None, zero_based=False):

        self.column_names = info_columns
        if sequence is not None and begin is not None and end is not None:
            seq_col = int(sequence) - 1
            start_col = int(begin) - 1
            end_col = int(end) - 1
        else:
            presets = self.determine_presets(file)
            seq_col = presets[0]
            start_col = presets[1]
            end_col = presets[2]
            start_offset = presets[3]


        if start_col < 0:
            msg = f"Invalid begin value: {begin}"
            sys.exit(msg)
        if end_col < 0:
            msg = f"Invalid end value: {end}"
            sys.exit(msg)

        self.features = []
        self.header = None
        self.rows = []

        rows = parse(file, 'tab')
        unique_id = 0
        start_offset = 0 if zero_based else 1
        for row in rows:

            #first line is the header
            if self.header is None:
                self.header = row
            else:
                self.rows.append(row)

                chr = row[seq_col]
                start = int(row[start_col]) - start_offset
                end = int(row[end_col])
                self.features.append((_Feature(chr, start, end), unique_id))
                unique_id += 1

    def to_JSON(self):


        obj = {
            "headers": ["unique_id"],
            "rows": []
        }

        if self.column_names is None:
            indeces = range(0, len(self.header))
        else:
            indeces = []
            for h in self.column_names:
                try:
                    idx = self.header.index(h)
                    indeces.append(idx)
                except:
                    print(f"Column {h} is not present")

        for i in indeces:
            obj["headers"].append(html.escape(self.header[i]))

        unique_id = 0
        for row in self.rows:
            r = [unique_id]
            for i in indeces:
                value = row[i] if i < len(row) else ""
                r.append(html.escape(value))
            obj["rows"].append(r)
            unique_id += 1

        return json.dumps(obj)

    def determine_presets(self, filename):

        filename = filename.lower()
        if (filename.endswith(".gz")):
            filename = filename[:-3]
        if filename.endswith(".bed"):
            return (0, 1, 2, True)
        elif filename.endswith(".gff") or filename.endswith("gff3") or filename.endswith("gtf"):
            return (0, 3, 4, False)
        elif filename.endswith(".maf"):
            return (4, 5, 6, False)
        else:
            msg = f"Unknown file format for: {filename} Please set --sequence, --start, and --end"
            sys.exit(msg)




class _Feature:

    def __init__(self, chr, start, end):
        self.chr = chr
        self.start = start
        self.end = end
