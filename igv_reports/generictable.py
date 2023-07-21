import json
import sys
import html
from .feature import parse


class GenericTable:

    @staticmethod
    def from_tabfile(file, info_columns=None, sequence=None, begin=None, end=None, zero_based=False):

        if sequence is not None and begin is not None and end is not None:
            seq_col = int(sequence) - 1
            start_col = int(begin) - 1
            end_col = int(end) - 1
        else:
            presets = determine_presets(file)
            seq_col = presets[0]
            start_col = presets[1]
            end_col = presets[2]
            zero_based = presets[3]

        if start_col < 0:
            msg = f"Invalid begin value: {begin}"
            sys.exit(msg)
        if end_col < 0:
            msg = f"Invalid end value: {end}"
            sys.exit(msg)

        regions = []
        header = None
        rows = parse(file, 'tab')
        header = None
        unique_id = 0
        start_offset = 0 if zero_based else 1
        for row in rows:
            # first line is the header
            if header is None:
                header = row
            else:
                chr = row[seq_col]
                start = int(row[start_col]) - start_offset
                end = int(row[end_col])
                regions.append((_Region(chr, start, end), unique_id))
                unique_id += 1

        return GenericTable(rows, regions, info_columns, header)

    @staticmethod
    def from_fusionjson(file):

        """
        Fusion json files have the following properties.  Not all are present
        {
            "# Long Reads": "305",
            "Annotations": "[\"INTRACHROMOSOMAL[chr11:0.01Mb]\",\"NEIGHBORS_OVERLAP:+:-:[5797]\"]",
            "Fusion": "BEST1--FTH1",
            "Left Breakpoint": "chr11:61965476:+",
            "Right Breakpoint": "chr11:61967627:-",
            "Splice Type": "INCL_NON_REF_SPLICE"
        }
        """

        with open(file) as json_file:

            j = json.load(json_file)

            header = j["columnns"] if "columns" in j else ['Fusion', "# Long Reads", 'Junction Reads',
                                                           'Spanning Fragments', "Expr Level (FFPM)", 'Splice Type',
                                                           'Left Gene', 'Left Breakpoint', 'Right Breakpoint',
                                                           "Annotations"]
            unique_id = 0
            features = []
            rows = []
            for record in j["fusions"]:
                row = []
                for h in header:
                    v = record[h] if h in record else ''
                    row.append(v)
                rows.append(row)

                chr = record["Fusion"]
                features.append((_Region(chr, None, None), unique_id))
                unique_id = unique_id + 1

        return GenericTable(rows, features, header, header)

    def __init__(self, rows, features, info_columns, header):

        self.column_names = info_columns
        self.features = features
        self.header = header
        self.rows = rows

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


def determine_presets(filename):
    filename = filename.lower()
    if (filename.endswith(".gz")):
        filename = filename[:-3]
    if filename.endswith(".bed"):
        return (0, 1, 2, True)
    elif filename.endswith(".gff") or filename.endswith("gff3") or filename.endswith("gtf"):
        return (0, 3, 4, False)
    elif filename.endswith(".maf"):
        return (4, 5, 6, False)
    elif filename.endswith(".mut"):
        return (0, 1, 2, False)
    else:
        msg = f"Unknown file format for: {filename} Please set --sequence, --start, and --end"
        sys.exit(msg)


class _Region:

    def __init__(self, chr, start = None, end = None):
        self.chr = chr
        self.start = start
        self.end = end
