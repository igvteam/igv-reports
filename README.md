# igv.js-reports

Python application to generate self-contained igv.js pages that can be opened within a browser with "file" protocol.   

## Installation

igv-reports requires Python 3.6 or greater and pysam version 0.15.1 or greater.  As with all python projects use of 
a virtual environment is reccommended.  We recommend the Anaconda distribution.  This will allow you
to install pysam as recommened below.   The steps below assume no Python is installed and used the Anaconda distribution, however
if Python is already installed and/or you prefer another distribution skip to the last step, ```pip install igv-reports```.

#### 1. Install Anaconda:  https://docs.anaconda.com/anaconda/

#### 2. Create a virtual environment

```html
conda create -n reports python=3.7.1
conda activate
conda install pip


```

#### 3. Install Pysam

igv.js-reports requires pysam.  From pysams [docs](https://pysam.readthedocs.io/en/latest/installation.html#installation);  _the recommended way to install pysam is through conda/bioconda_

```bash
conda config --add channels r
conda config --add channels bioconda
conda install pysam
```

As noted, _"This will install pysam from the bioconda channel and automatically makes sure that dependencies are installed. 
Also, compilation flags will be set automatically, which will potentially save a lot of trouble on OS X."_

At the current time installying pysam via pip often fails on OS X due to missing dependencies.

#### 4. Install igv-reports

```
pip install igv-reports

```

## Creating a variant report

A variant report consists of a table of variants and associated igv views for each variant.  Variant
reports are created with the script create_variant_report.py.  Command line arguments are described below.
Although _--tracks_ is optional, a typical report will include at least an alignment track
(BAM or CRAM) file from which the variants were called.  

**Arguments:**
* Required
    * variants    _vcf file defining variants_
    * fasta   _reference fasta file, must be indexed_
* Optional
    * --tracks _comma-delimited list of track files, see below for supported formats_
    * --ideogram _ideogram file in UCSC cytoIdeo format_
    * --template _html template file_
    * --output _output file name default="igvjs_viewer.html"_
    * --infoColumns _comma delimited list of VCF info field names to include in variant table_
    * --flanking _genomic region to include either side of variant, default=1000_
    * --standalone _embed all javascript referenced via ```<script>``` tags in the page_

**Track file formats:**

Currently supported track file formats are BAM, VCF, BED, GFF3, and GTF.   All files, with the exception of the
variants file, must be indexed.   Indexes for all supported formats can be created with pysam or samtools


#### Examples

Example:  Note: to run first replace <PATH to hg38.fa> with the path to a fasta for human assembly hg38

```bash

python create_variant_report.py \ 
examples/variants/cancer.vcf.gz \
https://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg38/hg38.fa \
--ideogram examples/variants/cytoBandIdeo.txt \
--flanking 1000 \
--infoColumns GENE,TISSUE,TUMOR,COSMIC_ID,GENE,SOMATIC \
--tracks examples/variants/recalibrated.bam,examples/variants/refgene.sort.bed.gz \
--output igvjs_viewer.html

```



## Creating a fusion inspector report 

Note: These instructions are specifically for Fusion Inspector reports.  See [https://github.com/FusionInspector/FusionInspector/wiki](https://github.com/FusionInspector/FusionInspector/wiki)

Fusion inspector reports are created by combining Fusion Inpsector output with an html template file.

First make sure that the html template file contains the comment line `<!-- start igv report here -->` within a script tag.
Directly below this line a javscript variable called "data" will be created so insure that no other variable names conflict.  
  
Then use the create_fusion_report.py script to create a new self-contained html file.
```sh
python create_fusion_report.py [filename]
```
where filename is the path to the igv.js html template file.  

To run the example execute

```sh
python create_fusion_report.py examples/fusions/igvjs_fusion.html
```

After, running the script, see examples/fusions/igvjs_fusion_viewer_report.html for the result.




## Converting a genomic data file to an igv.js Data URI

If you just want to get a data URI that can be read by igv.js in place of a url to a data file, use the get_datauri.py script
```sh
python igv_reports/get_datauri.py [filename]
```
The data uri will be printed to stdout.
