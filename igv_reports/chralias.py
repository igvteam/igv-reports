

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
    if c.startswith("chr"):
        if c == 'chrM':
            return 'chrM'
        else :
            return c[3:]
    else:
        if c == 'MT':
            return 'MT'
        else:
            return f'chr{c}'