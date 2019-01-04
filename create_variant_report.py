import argparse
from igv_reports import variant_report


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("variants", help="vcf file defining variants, required")
    parser.add_argument("fasta", help="reference fasta file, required")
    parser.add_argument("--ideogram", help="ideogram file in UCSC cytoIdeo format")
    parser.add_argument("--tracks", help="comma-delimited list of track files")
    parser.add_argument("--template", help="html template file", default=None)
    parser.add_argument("--output", help="output file name", default="igvjs_viewer.html")
    parser.add_argument("--infoColumns", help="comma delimited list of info column names for variant table")
    parser.add_argument("--flanking", help="genomic region to include either side of variant", default=1000)

    args = parser.parse_args()

    variant_report.create_report_from_vcf(args)
