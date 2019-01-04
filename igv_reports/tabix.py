import pysam

def get_data(filename, region):

    tb = pysam.TabixFile(filename)
    if region:
        range_string = region['chr'] + ":" + str(region['start']) + "-" + str(region['end'])
        it = tb.fetch(range_string)
    else:
        it = tb.fetch()

    data=""
    for row in it:
        data += row

    return data


