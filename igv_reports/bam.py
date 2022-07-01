import os
import pysam
from igv_reports import utils


def get_data(bam_file, region=None):
    args = ["-b", "-h", bam_file]
    if region:
        range_string = region['chr'] + ":" + str(region['start']) + "-" + str(region['end'])
        args.append(range_string)
    return pysam.view(*args)


# Return data in sam format -- for unit tests
def get_sam_data(bam_file, region=None):
    args = ["-h", bam_file]
    if region:
        range_string = region['chr'] + ":" + str(region['start']) + "-" + str(region['end'])
        args.append(range_string)
    return pysam.view(*args)


class BamReader:

    def __init__(self, filename, fasta=None):
        self.filename = filename
        self.fasta = fasta

    # add sam flag for unit tests
    def slice(self, region=None, reference=None, region2=None, split_bool=False, sam=False):
        args = ["-b", "-h", self.filename]
        if region:
            range_string = region['chr'] + ":" + str(region['start']) + "-" + str(region['end'])
            args.append(range_string)
        if self.fasta:
            args.append("-T" + self.fasta)

        if not split_bool:
            return pysam.view(*args)
        else:
            # This is complicated. We want BAM files with data from two
            # different references - one of the form chrA, another of the
            # form chr_A. This requires us to rename our coordinates (chr_A)
            # to match the BAM file (chrA), extract the BAM reads, convert
            # to SAM, replace the (chrA) by (chr_A), convert back to BAM, and
            # merge with original BAM.

            # obtain selections from BAM file
            args2 = ["-h", self.filename]
            if region2:
                range_string = utils.decode_chrom(region2['chr']) + ":" + str(region2['start']) + "-" + str(region2['end'])
                args2.append(range_string)
            if self.fasta:
                args2.append("-T" + self.fasta)

            # convert from chrA to chr_A and save to file for use by pysam
            extracted_sam2 = utils.encode_chrom(pysam.view(*args2))
            with open("temp.sam", "w") as f:
                f.write(extracted_sam2)

            # get non-headered uncompressed output for BAM1 and add to SAM2
            merged_sam = pysam.view("-h", "temp.sam")+pysam.view(*args[2:])

            # get coordinate parts of header from BAM1
            header = pysam.view(*args[1:]).split("\n")
            header = [line for line in header if "SN:chr" in line]

            # get merged SAM
            with open("temp_merged.sam", "w") as f:
                f.write("\n".join(header)+"\n")
                f.write(merged_sam)

            if not sam:
                output = pysam.view("-b", "-h", "temp_merged.sam")
            else:
                output = pysam.view("-h", "temp_merged.sam")

            # delete temp files
            if os.path.isfile("temp_merged.sam"):
                os.remove("temp_merged.sam")
            if os.path.isfile("temp.sam"):
                os.remove("temp.sam")

            return output
