import argparse
from igv_reports import report


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("variants", help="vcf file defining variants, required")
    parser.add_argument("fasta", help="reference fasta file, required")
    parser.add_argument("--ideogram", help="ideogram file in UCSC cytoIdeo format")
    parser.add_argument("--tracks", help="comma-delimited list of track files")
    parser.add_argument("--template", help="html template file", default=None)
    parser.add_argument("--output", help="output file name", default="igvjs_viewer.html")
    parser.add_argument("--infoColumns", help="comma delimited list of VCF info field names to include in variant table")
    parser.add_argument("--flanking", help="genomic region to include either side of variant", default=1000)
    parser.add_argument('--standalone', help='Print more data', action='store_true')
    args = parser.parse_args()

    report.create_report(args)
