# igv-reports

A Python application to generate self-contained HTML reports that consist of a table of genomic sites or regions and associated IGV views for each site.
The generated HTML page contains all data neccessary for IGV as uuencoded blobs. It can be opened within a web browser as a static page, with no depenency on the original input files.

## Installation

#### Prerequisites

igv-reports __requires Python 3.6__ or greater.  


#### Installing igv-reports

```bash
pip install igv-reports
```

igv-reports requires the package _pysam_ version 0.19.1 or greater, which should be installed automatically.  However on OSX this sometimes 
fails due to missing dependent libraries.  This can be fixed following the procedure below, from the pysam 
[docs](https://pysam.readthedocs.io/en/latest/installation.html#installation);  
_"The recommended way to install pysam is through conda/bioconda. 
This will install pysam from the bioconda channel and automatically makes sure that dependencies are installed. 
Also, compilation flags will be set automatically, which will potentially save a lot of trouble on OS X."_

```bash
conda config --add channels r
conda config --add channels bioconda
conda install pysam
```

## Creating a report

A report consists of a table of sites or regions and an associated IGV view for each site.  Reports are created with 
the command line script ```create_report```, or alternatively ```python igv_reports/report.py```.  Command line arguments are described below.
Although _--tracks_ is optional, a typical report will include at least an alignment track
(BAM or CRAM) file from which the variants were called.  

**Arguments:**
* Required
    * __sites__   VCF, BED, MAF, BEDPE, or generic tab delimited file of genomic variant sites.  Tabix indexed files are supported and strongly recommended for large files.
    * __fasta__   Reference fasta file; must be indexed.  This argument should be ommited if --genome is used, otherwise it is required.  
    
* The arguments _begin_, _end_, and _sequence_ are required for a generic tab delimited __sites__ file.
    * __--begin__ INT.   Column of start chromosomal position for __sites__ file.  Used for generic tab delimited input.
    * __--end__ INT.  Column of end chromosomal position for __sites__.  Used for generic tab delimited input.
    * __--sequence__ INT.   Column of sequence (chromosome) name.
    
* Optional for generic tab delimited __sites__ file
    * __--zero-based__  Specify that the position in the __sites__ file is 0-based (e.g. UCSC files) rather than 1-based.  Default is ```false```.

* Optional
    * __--genome__ **_New_** An igv.js genome identifier (e.g. hg38).  If supplied fasta, ideogram, and the default annotation track for the specified genome will be used.
    * __--ideogram__ FILE. Ideogram file in UCSC cytoIdeo format.  Useful when __fasta__ is used to specify the reference.
    * __--tracks__ LIST.  Space-delimited list of track files, see below for supported formats.  If both *tracks* and *track-config* are specified *tracks* will appear first by default.
    * __--track-config__  FILE.  File containing array of json configuration objects for igv.js tracks.  See the [igv.js wiki](https://github.com/igvteam/igv.js/wiki/Tracks-2.0) for more details.  This option allows customization of track parameters.  When using this option, the track ```url``` and ```indexURL``` properties should be set to the paths of the respective files.
    * __--roi__ LIST.  Space-delimited list of region-of-interest (ROI) files.  See [igv.js wiki](https://github.com/igvteam/igv.js/wiki/Regions-of-Interest).
    * __--template__ FILE. HTML template file.
    * __--output__ FILE. Output file name; default="igvjs_viewer.html".
    * __--info-columns__ LIST. Space delimited list of info field names to include in the variant table.  If __sites__ is a VCF file these are the info ID values.  If __sites__ is a tab delimited format these are column names.
    * __--info-columns-prefixes__ LIST. For VCF based reports only.  Space delimited list of prefixes of VCF info field IDs to include in the variant table.  Any info field with ID starting with one of the listed values will be included.
    * __--samples__ LIST.  Space delimited list of sample (i.e. genotypes) names.  Used in conjunction with __--sample-columns__.
    * __--sample-columns__ LIST. Space delimited list of VCF sample FORMAT field names to include in the variant table.  If __--samples__ is specified columns will be restricted to those samples, otherwise all samples will be included.
    * __--flanking__ INT. Genomic region to include either side of variant; default=1000.
    * __--standalone__ Embed all JavaScript referenced via ```<script>``` tags in the page.
    * __--sort__ Applies to alignment tracks only.  If specified alignments are initally sorted by the specified option. Supported values include  ```BASE, STRAND, INSERT_SIZE, MATE_CHR, and NONE```. Default value is ```BASE``` for single nucleotide variants, ```NONE``` (no sorting) otherwise.  See the igv.js documentation for more information.
    * __--exclude-flags__  INT. Value is passed to samtools as "-F" flag.  Used to filter alignments.  Default value is 1536 which filters alignments marked "duplicate" or "vendor failed". To include all alignments use ```--exclude-flags 0```.  See [samtools documentation](http://www.htslib.org/doc/samtools-view.html) for more details.
    * __--idlink__ URL tempate for information link for VCF ID values.  The token $$ will be substituted with the ID value.  Example: ```--idlink 'https://www.ncbi.nlm.nih.gov/snp/?term=$$'```
    * __--no-encode__ Don't embed data.  Fasta and track URLs are embedded unchanged.  The resulting report is depedendent on the original data files, which must be specified as URLs.  Local files are not supported with this option.

**Track file formats:**

Currently supported track file formats are BAM, CRAM, VCF, BED, GFF3, GTF, WIG, and BEDGRAPH.  FASTA. BAM, CRAM, and VCF  
files must be indexed.  Tabix is supported and it is recommended that all large files be indexed.   

## Examples

Data for the examples are available in the github repository [https://github.com/igvteam/igv-reports](https://github.com/igvteam/igv-reports).  The repository can be
downloaded as a zip archive here [https://github.com/igvteam/igv-reports/archive/refs/heads/master.zip](https://github.com/igvteam/igv-reports/archive/refs/heads/master.zip).
It is assumed that the examples are run from the root directory of the repository.  Output html is written to the [examples directory](https://github.com/igvteam/igv-reports/tree/master/examples) 
and can be viewed [here](https://igv.org/igv-reports/examples/1.5.1).

#### NEW (version 1.5.0) - Create a report using a genome identifier: ([Example output](https://igv.org/igv-reports/examples/1.5.1/example_genome.html)\)

```bash
create_report test/data/variants/variants.vcf.gz \
--genome hg38 \
--flanking 1000 \
--info-columns GENE TISSUE TUMOR COSMIC_ID GENE SOMATIC \
--tracks test/data/variants/variants.vcf.gz test/data/variants/recalibrated.bam \
--output examples/example_genome.html
```


#### Create a variant report from a VCF file: ([Example output](https://igv.org/igv-reports/examples/1.5.1/example_vcf.html))

```bash

create_report test/data/variants/variants.vcf.gz \
--fasta https://igv-genepattern-org.s3.amazonaws.com/genomes/seq/hg38/hg38.fa \
--ideogram test/data/hg38/cytoBandIdeo.txt \
--flanking 1000 \
--info-columns GENE TISSUE TUMOR COSMIC_ID GENE SOMATIC \
--samples reads_1_fastq \
--sample-columns DP GQ \
--tracks test/data/variants/variants.vcf.gz test/data/variants/recalibrated.bam test/data/hg38/refGene.txt.gz \
--output examples/example_vcf.html

```



#### Create a variant report with tracks defined in an [igv.js track config json file](https://github.com/igvteam/igv-reports/tree/master/test/data/variants/trackConfigs.json): ([Example output](https://igv.org/igv-reports/examples/1.5.1/example_config.html))

``` bash
create_report test/data/variants/variants.vcf.gz \
--fasta https://igv-genepattern-org.s3.amazonaws.com/genomes/seq/hg38/hg38.fa \
--ideogram test/data/hg38/cytoBandIdeo.txt \
--flanking 1000 \
--info-columns GENE TISSUE TUMOR COSMIC_ID GENE SOMATIC \
--track-config test/data/variants/trackConfigs.json \
--output examples/example_config.html
```


#### Create a variant report from a TCGA MAF file: ([Example output](https://igv.org/igv-reports/examples/1.5.1/example_maf.html))

```bash

create_report test/data/variants/tcga_test.maf \
--genome hg19 \
--flanking 1000 \
--info-columns Chromosome Start_position End_position Variant_Classification Variant_Type Reference_Allele Tumor_Seq_Allele1 Tumor_Seq_Allele2 dbSNP_RS \
--tracks test/data/variants/tcga_test.maf \
--output examples/example_maf.html

```

#### Create a variant report from a generic tab-delimited file: ([Example output](https://igv.org/igv-reports/examples/1.5.1/example_tab.html))

```bash

create_report test/data/variants/test.maflite.tsv \
--genome hg19 \
--sequence 1 --begin 2 --end 3 \
--flanking 1000 \
--info-columns chr start end ref_allele alt_allele \
--output examples/example_tab.html

```
####  Create a structural variant report from a bedpe file with two locations (BEDPE format): ([Example output](https://igv.org/igv-reports/examples/1.5.1/example_bedpe.html))

```bash

create_report test/data/variants/SKBR3_Sniffles_tra.bedpe \
--genome hg19 \
--flanking 1000 \
--tracks test/data/variants/SKBR3_Sniffles_variants_tra.vcf test/data/variants/SKBR3.ill.bam \
--output examples/example_bedpe.html
```

#### Create a variant report with custom ID link urls: ([Example output](https://igv.org/igv-reports/examples/1.5.1/example_idlink.html))

```bash

create_report test/data/variants/1kg_phase3_sites.vcf.gz \
--genome hg19 \
--flanking 1000 \
--tracks test/data/variants/1kg_phase3_sites.vcf.gz test/data/variants/NA12878_lowcoverage.bam \
--idlink 'https://www.ncbi.nlm.nih.gov/snp/?term=$$' \
--output examples/example_idlink.html

```

#### Create a junction report from a splice-junction bed file: ([Example output](https://igv.org/igv-reports/examples/1.5.1/example_junctions.html))

```bash
create_report test/data/junctions/Introns.38.bed \
--genome hg38 \
--type junction \
--track-config test/data/junctions/tracks.json \
--info-columns TCGA GTEx variant_name \
--title "Sample A" \
--output examples/example_junctions.html
```

#### Create a fusion report from a Trinity fusion json file: 

```bash
create_report test/data/fusion/igv.fusion_inspector_web.json \
--fasta test/data/fusion/igv.genome.fa  \
--template igv_reports/templates/fusion_template.html  \  
--track-config test/data/fusion/tracks.json  \
--output examples/example_fusion.html
```

#### Create a report containing wig and bedgraph files

```bash
create_report test/data/wig/regions.bed \
--genome hg19 \
--exclude-flags 512 \
--tracks test/data/wig/ucsc.bedgraph test/data/wig/mixed_step.wig test/data/wig/variable_step.wig \
--output examples/example_wig.html

```

#### Use of ```info-columns-prefixes``` option.  Variant track only, no alignments. ([Example output](https://igv.org/igv-reports/examples/1.5.1/example_ann.html))


```bash
python igv_reports/report.py test/data/annotated_vcf/consensus.filtered.ann.vcf \
--genome hg19 \
--flanking 1000 \
--info-columns cosmic_gene \
--info-columns-prefixes clinvar \
--tracks test/data/annotated_vcf/consensus.filtered.ann.vcf \
--output examples/example_ann.html 
```

#### Use ```--exclude-flags``` option to include duplicate alignments in report.  Default value is 1536 which filters duplicates and vendor-failed reads.

```bash
create_report test/data/dups/dups.bed \
--genome hg19 \
--exclude-flags 512 \
--tracks test/data/dups/dups.bam \
--output examples/example_dups.html
```

### Use ```-no-embed``` option to use external URL references for tracks in the report.  

```bash
create_report test/data/variants/variants.vcf.gz \
--genome hg38 \
--no-embed \
--tracks https://igv-genepattern-org.s3.amazonaws.com/test/reports/variants.vcf.gz https://igv-genepattern-org.s3.amazonaws.com/test/reports/recalibrated.bam \
--output examples/example_noembed.html

```

#### Converting genomic files to data URIs for use in igv.js 

The script ```create_datauri``` (```python igv_reports/datauri.py```) converts the contents of a file to a data uri for use in igv.js.   The datauri will be printed to stdout.  *NOTE* It is not neccessary to run this script explicitly to create a report, it is documented here
for use with stand-alone igv.js.   


**Convert a gzipped vcf file to a datauri.**

```bash
create_datauri test/data/variants/variants.vcf.gz

```

**Convert a slice of a local bam file to a datauri.**

```bash
create_datauri --region chr5:474,969-475,009 test/data/variants/recalibrated.bam 
```

**Convert a remote bam file to a datauri.**

```bash
create_datauri --region chr5:474,969-475,009 https://1000genomes.s3.amazonaws.com/phase3/data/NA12878/alignment/NA12878.mapped.ILLUMINA.bwa.CEU.low_coverage.20121211.bam
```




## [_Release Notes_](https://github.com/igvteam/igv-reports/releases)
