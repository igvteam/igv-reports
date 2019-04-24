import pysam

def get_data(bam_file, region=None):
    args = ["-b", "-h",  bam_file]
    if region:
        range_string = region['chr'] + ":" + str(region['start']) + "-" + str(region['end'])
        args.append(range_string)
    return pysam.view(*args)


class BamReader:

    def __init__(self, filename):

        self.filename = filename


    def slice(self, region = None) :
        args = ["-b", "-h",  self.filename]
        if region:
            range_string = region['chr'] + ":" + str(region['start']) + "-" + str(region['end'])
            args.append(range_string)
        return pysam.view(*args)