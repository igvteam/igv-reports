from igv_reports.chralias import get_alias
from igv_reports.stream import getstream

class IdeogramReader:

    def __init__(self, file):

        self.aliastable = {}
        self.ideogram_map = {}

        lastchr = None
        result = ''

        f = None
        try:
            f = getstream(file)
            for line in f:
                tokens = line.split('\t')
                chr = tokens[0]

                if not chr == lastchr:

                    if lastchr is not None:
                        self.ideogram_map[lastchr] = result
                        self.aliastable[get_alias(lastchr)] = lastchr

                    lastchr = chr
                    result = ''
                else:
                    result += line
        finally:
            if f:
                f.close()

        # final chr
        if lastchr is not None:
            self.ideogram_map[lastchr] = result
            self.aliastable[get_alias(lastchr)] = lastchr


    def get_data(self, chr):

        if chr in self.aliastable:
            chrname = self.aliastable[chr]
        else:
            chrname = chr

        if chrname in self.ideogram_map:
            return self.ideogram_map[chrname]
        else:
            return ''
