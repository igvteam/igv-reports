from . import regions
from pytwobit import TwoBit

from .chr_alias import get_chromosome_alias


class TwoBitReader:

    def __init__(self, path):
        self.path = path
        self.twobit = TwoBit(path)

    def slice(self, region):

        if isinstance(region,str):
            region = regions.parse_region(region)

        chr = region["chr"]
        start = None
        if region["start"] is not None:
            start = region["start"] - 1
        end = region["end"]

        data = self.twobit.fetch(chr, start, end)

        if data is None:
            chr = get_chromosome_alias(chr)
            data = self.twobit.fetch(chr, start, end)

        return data



