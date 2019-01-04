# igv.js-reports

Python application to generate dataURIs from genomic data files and self-contained igv.js pages that can
be opened within a browser with "file" protocol. 

**Requires Python 3.6**

## Installation

igv.js-reports requires pysam.  From pysams [docs](https://pysam.readthedocs.io/en/latest/installation.html#installation), the recoomended way to install pysam is through conda/bioconda

```bash
conda config --add channels r
conda config --add channels bioconda
conda install pysam
```

As noted, _"This will install pysam from the bioconda channel and automatically makes sure that dependencies are installed. 
Also, compilation flags will be set automatically, which will potentially save a lot of trouble on OS X."_

pip can sometimes be used, but at the current time often fails on a OS X due to missing denpendencies.

```sh
pip install pysam
```

## Creating a variant report

####Examples

Example 1:  Fill in path to fasta for human assembly hg38

```bash

python create_variant_report.py \ 
examples/variants/cancer.vcf.gz \
<PATH TO hg38.fa> \
--ideogram examples/variants/cytoBandIdeo.txt \
--flanking 1000 \
--infoColumns GENE,TISSUE,TUMOR,COSMIC_ID,GENE,SOMATIC \
--tracks examples/variants/recalibrated.bam,examples/variants/refgene.sort.bed.gz \
--output igvjs_viewer.html

```

Example 2

```bash
python create_variant_report.py  \ 
test/data/minigenome/variants.vcf.gz \ 
test/data/minigenome/minigenome.fa \
--flanking 1000 \
--tracks test/data/minigenome/alignments.bam,test/data/minigenome/annotations.gtf \
--output minigenome.html

```


## Creating a fusion inspector report from an existing html file

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
