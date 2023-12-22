echo genome
python igv_reports/report.py test/data/variants/variants.vcf.gz \
--genome hg38 \
--flanking 1000 \
--info-columns GENE TISSUE TUMOR COSMIC_ID GENE SOMATIC \
--tracks test/data/variants/variants.vcf.gz test/data/variants/recalibrated.bam \
--output docs/examples/example_genome.html

echo fasta
#### Create a variant report from a VCF file: ([Example output](https://igv.org/igv-reports/examples/1.5.1/example_vcf.html))
python igv_reports/report.py test/data/variants/variants.vcf.gz \
--fasta https://igv-genepattern-org.s3.amazonaws.com/genomes/seq/hg38/hg38.fa \
--ideogram test/data/hg38/cytoBandIdeo.txt \
--flanking 1000 \
--info-columns GENE TISSUE TUMOR COSMIC_ID GENE SOMATIC \
--samples reads_1_fastq \
--sample-columns DP GQ \
--tracks test/data/variants/variants.vcf.gz test/data/variants/recalibrated.bam test/data/hg38/refGene.txt.gz \
--output docs/examples/example_vcf.html


echo config
#### Create a variant report with tracks defined in an [igv.js track config json file](https://github.com/igvteam/igv-reports/tree/master/test/data/variants/trackConfigs.json): ([Example output](https://igv.org/igv-reports/examples/1.5.1/example_config.html))
python igv_reports/report.py test/data/variants/variants.vcf.gz \
--fasta https://igv-genepattern-org.s3.amazonaws.com/genomes/seq/hg38/hg38.fa \
--ideogram test/data/hg38/cytoBandIdeo.txt \
--flanking 1000 \
--info-columns GENE TISSUE TUMOR COSMIC_ID GENE SOMATIC \
--track-config test/data/variants/trackConfigs.json \
--output docs/examples/example_config.html

#### Create a variant report from a BED  file: ([Example output](https://igv.org/igv-reports/examples/1.5.1/example_bed.html))
echo bed
python igv_reports/report.py test/data/variants/variants.bed \
--genome hg38 \
--flanking 1000 \
--info-columns GENE TISSUE TUMOR COSMIC_ID GENE SOMATIC \
--tracks test/data/variants/variants.bed test/data/variants/recalibrated.bam \
--output docs/examples/example_bed.html


#### Create a variant report from a TCGA MAF file: ([Example output](https://igv.org/igv-reports/examples/1.5.1/example_bed.html))
echo maf
python igv_reports/report.py test/data/variants/tcga_test.maf \
--genome hg19 \
--flanking 1000 \
--info-columns Chromosome Start_position End_position Variant_Classification Variant_Type Reference_Allele Tumor_Seq_Allele1 Tumor_Seq_Allele2 dbSNP_RS \
--tracks test/data/variants/tcga_test.maf \
--output docs/examples/example_maf.html


#### Create a variant report from a generic tab-delimited file: ([Example output](https://igv.org/igv-reports/examples/1.5.1/example_tab.html))
echo tab
python igv_reports/report.py test/data/variants/test.maflite.tsv \
--genome hg19 \
--sequence 1 --begin 2 --end 3 \
--flanking 1000 \
--info-columns chr start end ref_allele alt_allele \
--output docs/examples/example_tab.html

####  Create a structural variant report for translocations from a vcf file with CHR2 and END info fields: ([Example output](https://igv.org/igv-reports/examples/1.5.1/example_tra_sv.html))
echo sv
python igv_reports/report.py test/data/variants/SKBR3_Sniffles_tra.vcf \
--genome hg19 \
--flanking 1000 \
--tracks test/data/variants/SKBR3_Sniffles_tra.vcf test/data/variants/SKBR3.ill.bam \
--output docs/examples/example_tra_sv.html

####  Create a structural variant report from a bedpe file with two locations (BEDPE format): ([Example output](https://igv.org/igv-reports/examples/1.5.1/example_bedpe.html))
echo bedpe
python igv_reports/report.py test/data/variants/SKBR3_Sniffles_tra.bedpe \
--genome hg19 \
--flanking 1000 \
--tracks test/data/variants/SKBR3_Sniffles_variants_tra.vcf test/data/variants/SKBR3.ill.bam \
--output docs/examples/example_bedpe.html


#### Create a variant report with custom ID link urls: ([Example output](https://igv.org/igv-reports/examples/1.5.1/example_idlink.html))

echo idlink

python igv_reports/report.py test/data/variants/1kg_phase3_sites.vcf.gz \
--genome hg19 \
--flanking 1000 \
--tracks test/data/variants/1kg_phase3_sites.vcf.gz test/data/variants/NA12878_lowcoverage.bam \
--idlink 'https://www.ncbi.nlm.nih.gov/snp/?term=$$' \
--output docs/examples/example_idlink.html


#### Create a junction report from a splice-junction bed file: ([Example output](https://igv.org/igv-reports/examples/1.5.1/example_junctions.html))

echo junctions
python igv_reports/report.py test/data/junctions/Introns.38.bed \
--genome hg38 \
--type junction \
--track-config test/data/junctions/tracks.json \
--info-columns TCGA GTEx variant_name \
--title "Sample A" \
--output docs/examples/example_junctions.html

#### Create a fusion report from a Trinity fusion json file: 

echo fusion
python igv_reports/report.py test/data/fusion/igv.fusion_inspector_web.json \
--fasta test/data/fusion/igv.genome.fa  \
--template igv_reports/templates/fusion_template.html  \
--track-config test/data/fusion/tracks.json  \
--output docs/examples/example_fusions.html


#### Create a report containing wig and bedgraph files

echo wig
python igv_reports/report.py test/data/wig/regions.bed \
--genome hg19 \
--exclude-flags 512 \
--tracks test/data/wig/ucsc.bedgraph test/data/wig/mixed_step.wig test/data/wig/variable_step.wig \
--output docs/examples/example_wig.html


#### Use of ```info-columns-prefixes``` option.  Variant track only, no alignments. ([Example output](https://igv.org/igv-reports/examples/1.5.1/example_ann.html))

echo ann
python igv_reports/report.py test/data/annotated_vcf/consensus.filtered.ann.vcf \
--genome hg19 \
--flanking 1000 \
--info-columns cosmic_gene \
--info-columns-prefixes clinvar \
--tracks test/data/annotated_vcf/consensus.filtered.ann.vcf \
--output docs/examples/example_ann.html


#### Use ```--exclude-flags``` option to include duplicate alignments in report.  Default value is 1536 which filters duplicates and vendor-failed reads.

echo dups
python igv_reports/report.py test/data/dups/dups.bed \
--genome hg19 \
--exclude-flags 512 \
--tracks test/data/dups/dups.bam \
--output docs/examples/example_dups.html


### Use ```-no-embed``` option to use external URL references for tracks in the report.  

echo no-embed
python igv_reports/report.py test/data/variants/variants.vcf.gz \
--genome hg38 \
--no-embed \
--tracks https://igv-genepattern-org.s3.amazonaws.com/test/reports/variants.vcf.gz https://igv-genepattern-org.s3.amazonaws.com/test/reports/recalibrated.bam \
--output docs/examples/example_noembed.html
