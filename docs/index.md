
## Examples

Data for the examples are available in the github repository [https://github.com/igvteam/igv-reports](https://github.com/igvteam/igv-reports). The repository can be
downloaded as a zip archive here [https://github.com/igvteam/igv-reports/archive/refs/heads/master.zip](https://github.com/igvteam/igv-reports/archive/refs/heads/master.zip).
It is assumed that the examples are run from the root directory of the repository. Output html is written to the
docs/examples directory.

#### Create a variant report from a VCF file: ([Example output](examples/example_vcf.html)) with title, header, and footer

create_reports test/data/variants/variants.vcf.gz \
--twobit https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.2bit \
--ideogram test/data/hg38/cytoBandIdeo.txt \
--flanking 1000 \
--info-columns GENE TISSUE TUMOR COSMIC_ID GENE SOMATIC \
--samples reads_1_fastq \
--sample-columns DP GQ \
--tracks test/data/variants/variants.vcf.gz test/data/variants/recalibrated.bam test/data/hg38/refGene.txt.gz \
--title "IGV Variant Inspector" \
--header test/example_header.html \
--footer test/example_footer.html \
--output docs/examples/example_vcf.html

#### Create a variant report from a VCF file with genotypes and sample information

#### VCF with genotypes and sample information
create_reports test/data/variants/1kg_genotypes.vcf \
--genome hg19 \
--sampleinfo test/data/variants/1kg_sampleinfo.txt \
--tracks test/data/variants/1kg_genotypes.vcf \
--output docs/examples/example_sampleinfo.html


#### Create a variant report from a BED  file: ([Example output](examples/example_bed.html))
create_reports test/data/variants/variants.bed \
--genome hg38 \
--flanking 1000 \
--tracks test/data/variants/variants.bed test/data/variants/recalibrated.bam \
--output docs/examples/example_bed.html


#### Create a variant report from a TCGA MAF file: ([Example output](examples/example_maf.html))

create_reports test/data/variants/tcga_test.maf \
--genome hg19 \
--flanking 1000 \
--info-columns Chromosome Start_position End_position Variant_Classification Variant_Type Reference_Allele Tumor_Seq_Allele1 Tumor_Seq_Allele2 dbSNP_RS \
--tracks test/data/variants/tcga_test.maf \
--output docs/examples/example_maf.html

#### Create a variant report from a generic tab-delimited file: ([Example output](examples/example_tab.html))

create_reports test/data/variants/test.maflite.tsv \
--genome hg19 \
--sequence 1 --begin 2 --end 3 \
--flanking 1000 \
--info-columns chr start end ref_allele alt_allele \
--output docs/examples/example_tab.html

#### Create a structural variant report from a vcf file with CHR2 and END info fields: ([Example output](examples/example_sv.html))

create_reports test/data/variants/SKBR3_Sniffles_tra.vcf \
--genome hg19 \
--flanking 1000 \
--maxlen 10500 \
--info-columns SVLEN \
--tracks test/data/variants/SKBR3_Sniffles_sv.vcf test/data/variants/SKBR3_translocations.ill.bam \
--output docs/examples/example_sv.html


#### Create a structural variant report from a bedpe file with two locations (BEDPE format): ([Example output](examples/example_bedpe.html))

create_reports test/data/variants/SKBR3_Sniffles_tra.bedpe \
--genome hg19 \
--flanking 1000 \
--tracks test/data/variants/SKBR3_Sniffles_variants_tra.vcf test/data/variants/SKBR3_translocations.ill.bam \
--output docs/examples/example_bedpe.html

#### Create a variant report with tracks defined in an [igv.js track config json file](https://github.com/igvteam/igv-reports/tree/master/test/data/variants/trackConfigs.json): ([Example output](examples/example_config.html))

create_reports test/data/variants/variants.vcf.gz \
--twobit --twobit https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.2bit \
--ideogram test/data/hg38/cytoBandIdeo.txt \
--flanking 1000 \
--info-columns GENE TISSUE TUMOR COSMIC_ID GENE SOMATIC \
--track-config test/data/variants/trackConfigs.json \
--output docs/examples/example_config.html

#### Create a variant report with custom ID link urls: ([Example output](examples/example_idlink.html))

create_reports test/data/variants/1kg_phase3_sites.vcf.gz \
--genome hg19 \
--flanking 1000 \
--tracks test/data/variants/1kg_phase3_sites.vcf.gz test/data/variants/NA12878_lowcoverage.bam \
--idlink 'https://www.ncbi.nlm.nih.gov/snp/?term=$$' \
--output docs/examples/example_idlink.html


#### Create a junction report from a splice-junction bed file: ([Example output](examples/example_junctions.html))

create_reports test/data/junctions/Introns.38.bed \
--genome hg38 \
--type junction \
--track-config test/data/junctions/tracks.json \
--info-columns TCGA GTEx variant_name \
--title "Sample A" \
--output docs/examples/example_junctions.html

#### Create a fusion report from a Trinity fusion json file:

create_reports test/data/fusion/igv.fusion_inspector_web.json \
--fasta test/data/fusion/igv.genome.fa  \
--template igv_reports/templates/fusion_template.html  \
--track-config test/data/fusion/tracks.json  \
--output docs/examples/example_fusions.html

#### Create a report containing wig and bedgraph files

create_reports test/data/wig/regions.bed \
--genome hg19 \
--exclude-flags 512 \
--tracks test/data/wig/ucsc.bedgraph test/data/wig/mixed_step.wig test/data/wig/variable_step.wig \
--output docs/examples/example_wig.html

#### Use of ```info-columns-prefixes``` option. Variant track only, no alignments. ([Example output](examples/example_ann.html))

create_reports test/data/annotated_vcf/consensus.filtered.ann.vcf \
--genome hg19 \
--flanking 1000 \
--info-columns cosmic_gene \
--info-columns-prefixes clinvar \
--tracks test/data/annotated_vcf/consensus.filtered.ann.vcf \
--output docs/examples/example_ann.html


#### Create a variant report from a VCF file with Tabulator Template: ([Example output](examples/example_vcf_tabulator.html))

create_reports test/data/variants/variants.vcf.gz \
--genome  hg38  \
--ideogram test/data/hg38/cytoBandIdeo.txt \
--flanking 1000 \
--info-columns GENE TISSUE TUMOR COSMIC_ID GENE SOMATIC \
--samples reads_1_fastq \
--sample-columns DP GQ \
--tracks test/data/variants/variants.vcf.gz test/data/variants/recalibrated.bam \
--tabulator \
--filter-config test/data/variants/filter_config.yaml \
--output docs/examples/example_vcf_tabulator.html

#### Use ```--exclude-flags``` option to include duplicate alignments in report by specifying a samtools `--exclude-flags` value. Default value is 1536 which filters duplicates and vendor-failed reads.

create_reports test/data/dups/dups.bed \
--genome hg19 \
--exclude-flags 512 \
--tracks test/data/dups/dups.bam \
--output docs/examples/example_dups.html

### Use ```-no-embed``` option to use external URL references for tracks in the report.

create_reports test/data/variants/variants.vcf.gz \
--genome hg38 \
--no-embed \
--tracks https://raw.githubusercontent.com/igvteam/igv-reports/refs/heads/master/test/data/variants/variants.vcf.gz https://raw.githubusercontent.com/igvteam/igv-reports/refs/heads/master/test/data/variants/recalibrated.bam \
--output docs/examples/example_noembed.html
