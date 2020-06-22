# igv-reports

Python application to generate self-contained igv.js pages that can be opened within a browser with "file" protocol. 
The generated html page contains all data neccessary for IGV as uuencoded blobs.  

## Installation

#### Prerequisites

igv-reports requires Python 3.6 or greater and pip.  As with all Python projects use of a virtual enviornment is recommended.
Instructions for creating a virtual environment using _conda_ are [below](#creating-a-virtual-environment) 


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

A report consists of a table of sites or regions and an associated igv views for each site.  Reports are created with 
the command line script ```create_report```.  Command line arguments are described below.
Although _--tracks_ is optional, a typical report will include at least an alignment track
(BAM or CRAM) file from which the variants were called.  

**Arguments:**
* Required
    * sites    _vcf or bed file of genomic sites_
    * fasta   _reference fasta file, must be indexed_
* Optional
    * --tracks _space-delimited list of track files, see below for supported formats.  If both *tracks* and *track-config* are specified *tracks* will appear first._
    * --track-confg _file containing array of json configuration objects for igv.js tracks.  see the [igv.js wiki](https://github.com/igvteam/igv.js/wiki/Tracks-2.0) for more details.  This option allows customization of track parameters._
    * --ideogram _ideogram file in UCSC cytoIdeo format_
    * --template _html template file_
    * --output _output file name default="igvjs_viewer.html"_
    * --info-columns _space delimited list of VCF info field names to include in variant table_
    * --info-columns-prefixes _space delimited list of prefixes of VCF info field names to include in variant table_
    * --sample-columns _space delimited list of VCF sample/format field names to include in variant table_
    * --flanking _genomic region to include either side of variant, default=1000_
    * --standalone _embed all javascript referenced via ```<script>``` tags in the page_

**Track file formats:**

Currently supported track file formats are BAM, CRAM, VCF, BED, GFF3, and GTF.  FASTA. BAM, CRAM, and VCF  files must 
be indexed.  Tabix is supported for other file types and it is recommended that all large files be indexed.   

## Examples

Data for the examples are available for [download](https://s3.amazonaws.com/igv.org.test/reports/examples.zip).

#### Creating a variant report from a VCF file:  

```bash

create_report examples/variants/variants.vcf.gz https://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg38/hg38.fa --ideogram examples/variants/cytoBandIdeo.txt --flanking 1000 --info-columns GENE TISSUE TUMOR COSMIC_ID GENE SOMATIC --tracks examples/variants/variants.vcf.gz examples/variants/recalibrated.bam examples/variants/refGene.sort.bed.gz --output igvjs_viewer.html

```

#### Createing a junction report from a splice-junction bed file

```bash
create_report examples/junctions/Introns.38.bed https://s3.dualstack.us-east-1.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg38/hg38.fa --type junction --ideogram examples/junctions/cytoBandIdeo.txt --output junctions.html --track-config examples/junctions/tracks.json --info-columns TCGA GTEx variant_name --title "Sample A"
```

#### Converting genomic files to data URIs for use in igv.js 

The script ```create_datauri`` converts the contents of a file to a data uri for use in igv.js.   The datauri will be
printed to stdout.  *NOTE* It is not neccessary to run this script explicitly to create a report, it is documented here
for use with stand-alone igv.js.   



**Convert a gzipped vcf file to a datauri.**

```bash
create_datauri examples/variants/variants.vcf.gz

```

**Convert a slice of a remote cram file to a datauri.**

```bash
create_datauri \
--region 8:127,738,322-127,738,508 \
https://s3.amazonaws.com/1000genomes/data/HG00096/alignment/HG00096.alt_bwamem_GRCh38DH.20150718.GBR.low_coverage.cram 
```


## Creating a virtual environment

Instructions for creating a virtual environment using ```conda``` follow.

#### 1. Install Anaconda:  https://docs.anaconda.com/anaconda/

#### 2. Create a virtual environment

```bash
conda create -n myenv python=3.7.1
conda install -n myenv pip
conda activate
conda install pip
```
