
def merge_regions(regions, threhold = 500):

    region_structs = []

    for r in regions:
        region_structs.append(parse_region(r))

    # build dictionary of regions by chromosome
    region_dict =  dict();
    for r in region_structs:
        chr = r['chr']
        if chr not in region_dict:
            region_dict[chr] = []
        region_dict[chr].append(r)

    merged_regions = []
    values = region_dict.values()
    for region_list in values:
        if len(region_list) == 1:
            merged_regions.append(region_list[0])
        else:
            region_list.sort(key=lambda r: r['start'])
            n = len(region_list)
            last_region = region_list[0]

            for i in range(1, n):
                reg = region_list[i]
                if reg['start'] - last_region['end'] < threhold:
                    last_region['end'] = max(last_region['end'], reg['end'])
                else:
                    merged_regions.append(last_region)
                    last_region = reg

            merged_regions.append(last_region)

    return merged_regions


def parse_region(locus_string):

    tokens = locus_string.split(":")
    chr = tokens[0]

    t2 = tokens[1].split('-')
    start = int(t2[0].replace(',', ''))
    if len(t2) > 1:
        end = int(t2[1].replace(',',''))
    else:
        end = start

    return {'chr': chr, 'start': start, 'end': end}