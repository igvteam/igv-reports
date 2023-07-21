# Run from root directory in development mode
echo "vcf"
python igv_reports/report.py test/data/variants/variants.vcf.gz http://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg38/hg38.fa --ideogram test/data/hg38/cytoBandIdeo.txt --flanking 1000 --info-columns GENE TISSUE TUMOR COSMIC_ID GENE SOMATIC --tracks test/data/variants/variants.vcf.gz test/data/variants/recalibrated.bam test/data/hg38/refGene.txt.gz --output examples/example_vcf.html
echo "config"
python igv_reports/report.py test/data/variants/variants.vcf.gz http://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg38/hg38.fa --ideogram test/data/hg38/cytoBandIdeo.txt --flanking 1000 --info-columns GENE TISSUE TUMOR COSMIC_ID GENE SOMATIC --track-config test/data/variants/trackConfigs.json --output examples/example_config.html
echo "maf"
python igv_reports/report.py test/data/variants/tcga_test.maf http://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg19/hg19.fasta --ideogram test/data/hg19/cytoBandIdeo.txt --flanking 1000 --info-columns Chromosome Start_position End_position Variant_Classification Variant_Type Reference_Allele Tumor_Seq_Allele1 Tumor_Seq_Allele2 dbSNP_RS --tracks test/data/variants/tcga_test.maf https://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/refGene.txt.gz --output examples/example_maf.html
echo "tab"
python igv_reports/report.py test/data/variants/test.maflite.tsv http://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg19/hg19.fasta --ideogram test/data/hg19/cytoBandIdeo.txt --flanking 1000 --sequence 1 --begin 2 --end 3 --info-columns chr start end ref_allele alt_allele --tracks https://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/refGene.txt.gz --output examples/example_tab.html
echo "bedpe"
python igv_reports/report.py test/data/variants/SKBR3_Sniffles_tra.bedpe http://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg19/hg19.fasta --ideogram test/data/hg19/cytoBandIdeo.txt --flanking 1000 --tracks test/data/variants/SKBR3_Sniffles_variants_tra.vcf test/data/variants/SKBR3.ill.bam https://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/refGene.txt.gz --output examples/example_bedpe.html
echo "idlink"
python igv_reports/report.py test/data/variants/1kg_phase3_sites.vcf.gz http://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg19/hg19.fasta --ideogram test/data/hg19/cytoBandIdeo.txt --flanking 1000 --tracks test/data/variants/1kg_phase3_sites.vcf.gz test/data/variants/NA12878_lowcoverage.bam https://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/refGene.txt.gz --idlink 'https://www.ncbi.nlm.nih.gov/snp/?term=$$' --output examples/example_idlink.html
echo "junctions"
python igv_reports/report.py test/data/junctions/Introns.38.bed http://s3.dualstack.us-east-1.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg38/hg38.fa --type junction --ideogram test/data/hg38/cytoBandIdeo.txt --output examples/example_junctions.html --track-config test/data/junctions/tracks.json --info-columns TCGA GTEx variant_name --title "Sample A"
echo "genome"
python igv_reports/report.py test/data/variants/variants.vcf.gz --genome hg38 --flanking 1000 --info-columns GENE TISSUE TUMOR COSMIC_ID GENE SOMATIC --tracks test/data/variants/variants.vcf.gz test/data/variants/recalibrated.bam --output examples/example_genome.html
echo "ann"
python igv_reports/report.py test/data/annotated_vcf/consensus.filtered.ann.vcf --genome hg19 --flanking 1000 --info-columns cosmic_gene --info-columns-prefixes clinvar --tracks test/data/annotated_vcf/consensus.filtered.ann.vcf --output examples/example_ann.html
echo "softclip"
python igv_reports/report.py test/data/softclip/variant.bed --genome hg19 --flanking 1000 --track-config test/data/softclip/trackconfig.json --output examples/example_softclip.html
echo "dups"
python igv_reports/report.py test/data/dups/dups.bed --genome hg19 --flanking 1000 --tracks test/data/dups/dups.bam --exclude-flags 512 --output  examples/example_dups.html
echo "wig"
python igv_reports/report.py test/data/wig/regions.bedpe --genome hg19 --exclude-flags 512 --tracks test/data/wig/ucsc.bedgraph test/data/wig/mixed_step.wig test/data/wig/variable_step.wig --output examples/example_wig.html
echo "noembd"
python igv_reports/report.py test/data/variants/variants.vcf.gz --genome hg38 --no-embed --flanking 1000 --info-columns GENE TISSUE TUMOR COSMIC_ID GENE SOMATIC --samples reads_1_fastq --sample-columns DP GQ --tracks https://igv-genepattern-org.s3.amazonaws.com/test/reports/variants.vcf.gz https://igv-genepattern-org.s3.amazonaws.com/test/reports/recalibrated.bam --output examples/example_noembed.html
echo "fusions"
python igv_reports/report.py test/data/fusion/igv.fusion_inspector_web.json test/data/fusion/igv.genome.fa  --template igv_reports/templates/fusion_template.html  --track-config test/data/fusion/tracks.json  --output examples/example_fusion.html
