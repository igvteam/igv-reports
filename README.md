# igv-reports

Python application to generate self-contained igv.js pages that can be opened within a browser with "file" protocol. 
The generated html page contains all data neccessary for IGV as uuencoded blobs.  

## Installation

#### Prerequisites

igv-reports __requires Python 3.6__ or greater and __pip__.  

As with all Python projects, use of a __virtual environment__ is recommended.
Instructions for creating a virtual environment using ```conda``` follow.

__1.__ Install Anaconda from https://docs.anaconda.com/anaconda/

__2.__ Create a virtual environment

```bash
conda create -n myenv python=3.7.1
conda install -n myenv pip
conda activate myenv
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
    * __sites__    VCF or BED file of genomic sites.
    * __fasta__   Reference fasta file; must be indexed.
* Optional
    * __--tracks__ Space-delimited list of track files, see below for supported formats.  If both *tracks* and *track-config* are specified *tracks* will appear first.
    * __--track-confg__ File containing array of json configuration objects for igv.js tracks.  See the [igv.js wiki](https://github.com/igvteam/igv.js/wiki/Tracks-2.0) for more details.  This option allows customization of track parameters.
    * __--ideogram__ Ideogram file in UCSC cytoIdeo format.
    * __--template__ HTML template file.
    * __--output__ Output file name; default="igvjs_viewer.html".
    * __--info-columns__ Space delimited list of VCF info field names to include in variant table.
    * __--info-columns-prefixes__ Space delimited list of prefixes of VCF info field names to include in variant table.
    * __--sample-columns__ Space delimited list of VCF sample/format field names to include in variant table.
    * __--flanking__ Genomic region to include either side of variant; default=1000.
    * __--standalone__ Embed all JavaScript referenced via ```<script>``` tags in the page.

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

The script ```create_datauri``` converts the contents of a file to a data uri for use in igv.js.   The datauri will be
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
