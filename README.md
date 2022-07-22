# igv-reports

A Python application to generate self-contained HTML reports that consist of a table of genomic sites or regions and associated IGV views for each site.
The generated HTML page contains all data neccessary for IGV as uuencoded blobs. It can be opened within a web browser as a static page, with no depenency on the original input files.


## Installation

#### Prerequisites

igv-reports __requires Python 3.6__ or greater and __pip__.  

As with all Python projects, use of a __virtual environment__ is recommended.
Instructions for creating a virtual environment using ```conda``` follow.

__1.__ Install Anaconda from https://docs.anaconda.com/anaconda/

__2.__ Create a virtual environment

```bash
conda create -n igvreports python=3.7.1
conda activate igvreports
```

#### Installing igv-reports

```bash
pip install igv-reports
```

igv-reports requires the package _pysam_ which should be installed automatically.  However on OSX this sometimes 
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

A report consists of a table of sites or regions and an associated IGV views for each site.  Reports are created with 
the command line script ```create_report```.  Command line arguments are described below.
Although _--tracks_ is optional, a typical report will include at least an alignment track
(BAM or CRAM) file from which the variants were called.  

**Arguments:**
* Required
    * __sites__   VCF, BED, MAF, or generic tab delimited file of genomic variant sites.  Tabix indexed files are supported and strongly recommended for large files.  The tabix index is not specified, but inferred by convention (adding ".tbi" to the end of the bgzipped variant file).
    * __fasta__   Reference fasta file; must be indexed.
    
* Required for generic tab delimited __sites__ file
    * __--begin__ INT.   Column of start chromosomal position for __sites__ file.  Used for generic tab delimited input.
    * __--end__ INT.  Column of end chromosomal position for __sites__.  Used for generic tab delimited input.
    * __--sequence__ INT.   Column of sequence (chromosome) name.
    
* Optional for generic tab delimited __sites__ file
    * __--zero-based__  Specify that the position in the __sites__ file is 0-based (e.g. UCSC files) rather than 1-based.  Default is ```false```.

* Optional
    * __--tracks__ LIST.  Space-delimited list of track files, see below for supported formats.  If both *tracks* and *track-config* are specified *tracks* will appear first by default.
    * __--track-config__  FILE.  File containing array of json configuration objects for igv.js tracks.  See the [igv.js wiki](https://github.com/igvteam/igv.js/wiki/Tracks-2.0) for more details.  This option allows customization of track parameters.  When using this option, the track ```url``` and ```indexURL``` properties should be set to the paths to the respective files.
    * __--ideogram__ FILE. Ideogram file in UCSC cytoIdeo format.
    * __--template__ FILE. HTML template file.
    * __--output__ FILE. Output file name; default="igvjs_viewer.html".
    * __--info-columns__ LIST. Space delimited list of field names to include in the variant table.  If __sites_ is a VCF file these are the info field names.  If __sites__ is a tab delimited format these are column names.
    * __--info-columns-prefixes__ LIST. Space delimited list of prefixes of VCF info field names to include in variant table.
    * __--sample-columns__ LIST. Space delimited list of VCF sample/format field names to include in variant table.
    * __--flanking__ INT. Genomic region to include either side of variant; default=1000.
    * __--standalone__ Embed all JavaScript referenced via ```<script>``` tags in the page.
    * __--sort__ Applies to alignment tracks only.  If specified alignments are initally sorted by the specified option. Supported values include  ```BASE, STRAND, INSERT_SIZE, MATE_CHR, and NONE```. Default value is ```BASE``` for single nucleotide variants, ```NONE``` (no sorting) otherwise.  See the igv.js documentation for more information.
    * __--idlink__ URL tempate for information link for VCF ID values.  The token $$ will be substituted with the ID value.  Example: ```--idlink 'https://www.ncbi.nlm.nih.gov/snp/?term=$$'```
     
**Tab delimited __sites__ file**

Variant sites can be defined from a [VCF](https://samtools.github.io/hts-specs/VCFv4.2.pdf),  
UCSC [BED](https://genome.ucsc.edu/FAQ/FAQformat.html#format1), or a generic tab delimited file.   
**Now also supported: BEDPE format for structural variants**

Note: VCF files must be tabix indexed, and must end with a ".gz" extension.  The ".bgz" extension is not supported.

**Track file formats:**

Currently supported track file formats are BAM, CRAM, VCF, BED, GFF3, and GTF.  FASTA. BAM, CRAM, and VCF  files must 
be indexed.  Tabix is supported for other file types and it is recommended that all large files be indexed.   

## Examples

Data for the examples are available in the github repository [https://github.com/igvteam/igv-reports](https://github.com/igvteam/igv-reports).  The repository can be
downloaded as a zip archive here [https://github.com/igvteam/igv-reports/archive/refs/tags/v1.0.5.zip](https://github.com/igvteam/igv-reports/archive/refs/heads/master.zip).
It is assumed that the examples are run from the root directory of the repository.

#### Creating a variant report from a VCF file: \([Link to example output](examples/results/example1.html)\)

```bash

create_report examples/variants/variants.vcf.gz http://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg38/hg38.fa --ideogram examples/variants/cytoBandIdeo_hg38.txt --flanking 1000 --info-columns GENE TISSUE TUMOR COSMIC_ID GENE SOMATIC --tracks examples/variants/variants.vcf.gz examples/variants/recalibrated.bam examples/variants/refGene.sort.bed.gz --output example1.html

```

#### Creating a variant report from a "track-config" json file: \([Link to example output](examples/results/example_config.html)\)

``` bash
create_report examples/variants/variants.vcf.gz http://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg38/hg38.fa --ideogram examples/variants/cytoBandIdeo_hg38.txt --flanking 1000 --info-columns GENE TISSUE TUMOR COSMIC_ID GENE SOMATIC --track-config examples/variants/trackConfigs.json --output example_config.html
```


#### Creating a variant report from a TCGA MAF file: \([Link to example output](examples/results/example_maf.html)\)

```bash

create_report examples/variants/tcga_test.maf http://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg19/hg19.fasta --ideogram examples/variants/cytoBandIdeo_hg19.txt --flanking 1000 --info-columns Chromosome Start_position End_position Variant_Classification Variant_Type Reference_Allele Tumor_Seq_Allele1 Tumor_Seq_Allele2 dbSNP_RS --tracks  examples/variants/refGene.sort.bed.gz --output example_maf.html

```

#### Creating a variant report from a generic tab-delimited file: \([Link to example output](examples/results/example_tab.html)\)

```bash

create_report examples/variants/test.maflite.tsv http://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg19/hg19.fasta --ideogram examples/variants/cytoBandIdeo_hg19.txt --flanking 1000 --sequence 1 --begin 2 --end 3 --info-columns chr start end ref_allele alt_allele --tracks examples/variants/refGene.sort.bed.gz --output example_tab.html

```
#### Creating a variant report from a bedpe file with two locations (BEDPE format): \([Link to example output](examples/results/example_bedpe.html)\)

```bash

create_report examples/variants/SKBR3_Sniffles_tra.bedpe http://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg19/hg19.fasta --ideogram examples/variants/cytoBandIdeo_hg19.txt --flanking 1000 --tracks examples/variants/SKBR3.ill.bam examples/variants/refGene.sort.bed.gz --output example_bedpe.html

```

#### Creating a variant report from a vcf file with custom ID link urls: \([Link to example output](examples/results/example_idlink.html)\)

```bash

create_report examples/variants/1kg_phase3_sites.vcf.gz http://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg19/hg19.fasta --ideogram examples/variants/cytoBandIdeo_hg19.txt --flanking 1000 --tracks examples/variants/1kg_phase3_sites.vcf.gz examples/variants/NA12878_lowcoverage.bam examples/variants/refGene.sort.bed.gz --idlink 'https://www.ncbi.nlm.nih.gov/snp/?term=$$' --output example_idlink.html

```

#### Creating a junction report from a splice-junction bed file: \([Link to example output](examples/results/example_junctions.html)\)

```bash
create_report examples/junctions/Introns.38.bed http://s3.dualstack.us-east-1.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg38/hg38.fa --type junction --ideogram examples/junctions/cytoBandIdeo_hg38.txt --output example_junctions.html --track-config examples/junctions/tracks.json --info-columns TCGA GTEx variant_name --title "Sample A"
```


#### Converting genomic files to data URIs for use in igv.js 

The script ```create_datauri``` converts the contents of a file to a data uri for use in igv.js.   The datauri will be
printed to stdout.  *NOTE* It is not neccessary to run this script explicitly to create a report, it is documented here
for use with stand-alone igv.js.   



**Convert a gzipped vcf file to a datauri.**

```bash
create_datauri examples/variants/variants.vcf.gz

```

**Convert a slice of a remote cram file to a cram datauri.**

```bash
create_datauri \
--region 8:127,738,322-127,738,508 \
http://s3.amazonaws.com/1000genomes/data/HG00096/alignment/HG00096.alt_bwamem_GRCh38DH.20150718.GBR.low_coverage.cram 
```



## [_Release Notes_](https://github.com/igvteam/igv-reports/releases)
