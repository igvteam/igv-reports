from .chr_alias import get_chromosome_alias

def build_aliastable(chrs):

    chralias = {}

    for c in chrs:

        if c.startswith("chr"):
            if c == 'chrM':
                chralias['MT'] = 'chrM'
            else :
                alias = c[3:]
                chralias[alias] = c
        else:
            if c == 'MT':
                chralias['chrM'] = 'MT'
            else:
                alias = f'chr{c}'
                chralias[alias] = c

    return chralias


def get_alias(c):
    """
    Return the alias for a chromosome name, e.g. chr1 <-> 1, chrM <-> MT.
    """
    return get_chromosome_alias(c)