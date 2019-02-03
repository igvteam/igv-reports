#!/bin/sh
python ../create_variant_report.py \
https://s3.amazonaws.com/igv.org.test/reports/variants/cancer.vcf.gz \
https://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg38/hg38.fa \
--ideogram variants/cytoBandIdeo.txt  \
--flanking 1000 \
--infoColumns GENE,TISSUE,TUMOR,COSMIC_ID,GENE,SOMATIC \
--tracks https://s3.amazonaws.com/igv.org.test/reports/variants/recalibrated.bam,variants/refgene.sort.bed.gz \
--output igvjs_viewer.html
