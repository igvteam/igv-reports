# igv-reports

igv-reports - A Python application to generate self-contained HTML reports for variant review and other genomic
applications. Reports consist of a table of genomic sites and an embedded IGV genome browser for viewing data for each
site. The tool extracts slices of data for each site and embeds the data as blobs in the HTML report file. The report
can be opened in a web browser as a static page, with no depenency on the original input files.

## Installation

#### Prerequisites

igv-reports __requires Python 3.8__ or greater.

#### Installing igv-reports

```bash
pip install igv-reports
```

igv-reports requires the package _pysam_ version 0.22.0 or greater, which should be installed automatically. However, on
OSX this sometimes fails due to missing dependent libraries. This can be fixed following the procedure below, from the
pysam [docs](https://pysam.readthedocs.io/en/latest/installation.html#installation);  
_"The recommended way to install pysam is through conda/bioconda.
This will install pysam from the bioconda channel and automatically makes sure that dependencies are installed.
Also, compilation flags will be set automatically, which will potentially save a lot of trouble on OS X."_

```bash
conda config --add channels r
conda config --add channels bioconda
conda install pysam
```

## Creating a report

Reports are created with the command line script ```create_report```, or
alternatively ```python igv_reports/report.py```. Command line arguments
are described below. Although _--tracks_ is optional, a typical report will include at least an alignment track
(BAM or CRAM) file from which the variants were called.

**Arguments:**

* Required
    * __sites__   VCF, BED, MAF, BEDPE, or generic tab delimited file of genomic variant sites. Tabix indexed files are
      supported and strongly recommended for large files.
    * __--fasta__   Reference fasta file; must be indexed. One of either --fasta, --twobit, or --genome is required.
    * __--twobit__  Reference twobit sequence file.
    * __--genome__  An igv.js genome identifier (e.g. hg38). If supplied sequence, ideogram, and the default annotation
      track for the specified genome will be used.*

* The arguments _begin_, _end_, and _sequence_ are required for a generic tab delimited __sites__ file.
    * __--begin__ INT. Column of start chromosomal position for __sites__ file. Used for generic tab delimited input.
    * __--end__ INT. Column of end chromosomal position for __sites__. Used for generic tab delimited input.
    * __--sequence__ INT. Column of sequence (chromosome) name.

* Optional coordinate system flag for generic tab delimited __sites__ file only
    * __--zero_based__  Specify that the position in the __sites__ file is 0-based (e.g. UCSC files) rather than
      1-based. Default is ```false```.

* Optional
    * __--ideogram__ FILE. Ideogram file in UCSC cytoIdeo format. Useful when __fasta__ is used to specify the
      reference.
    * __--tracks__ LIST. Space-delimited list of track files, see below for supported formats. If both *tracks* and
      *track-config* are specified *tracks* will appear first by default.
    * __--track-config__  FILE. File containing array of json configuration objects for igv.js tracks. See
      the [igv.js documentation](https://github.com/igvteam/igv.js/wiki/Tracks-2.0) for more details. This option allows
      customization of track parameters. When using this option, the track ```url``` and ```indexURL``` properties
      should be set to the paths of the respective files.
    * __--roi__ LIST. Space-delimited list of region-of-interest (ROI) files. See
      the [igv.js documentation](https://igv.org/doc/igvjs/#Regions-of-Interest/).
    * __--sampleinfo__ LIST. Space delimited list of sample information files. See
      the [igv.js documentation](https://igv.org/doc/igvjs/#SampleInfo/).
    * __--template__ FILE. HTML template file.
    * __--output__ FILE. Output file name; default="igvjs_viewer.html".
    * __--info-columns__ LIST. Space delimited list of info field names to include in the variant table. If __sites__ is
      a VCF file these are the info ID values. If __sites__ is a tab delimited format these are column names.
    * __--info-columns-prefixes__ LIST. For VCF based reports only. Space delimited list of prefixes of VCF info field
      IDs to include in the variant table. Any info field with ID starting with one of the listed values will be
      included.
    * __--samples__ LIST. Space delimited list of sample (i.e. genotypes) names. Used in conjunction with _
      _--sample-columns__.
    * __--sample-columns__ LIST. Space delimited list of VCF sample FORMAT field names to include in the variant table.
      If __--samples__ is specified columns will be restricted to those samples, otherwise all samples will be included.
    * __--flanking__ INT. Genomic region to include either side of variant; default=1000.
    * __--standalone__ Embed all JavaScript referenced via ```<script>``` tags in the page.
    * __--sort__ Applies to alignment tracks only. If specified alignments are initally sorted by the specified option.
      Supported values include  ```BASE, STRAND, INSERT_SIZE, MATE_CHR, and NONE```. Default value is ```BASE``` for
      single nucleotide variants, ```NONE``` (no sorting) otherwise. See the igv.js documentation for more information.
    * __--exclude-flags__  INT. Value is passed to samtools as "-F" flag. Used to filter alignments. Default value is
      1536 which filters alignments marked "duplicate" or "vendor failed". To include all alignments
      use ```--exclude-flags 0```. See [samtools documentation](http://www.htslib.org/doc/samtools-view.html) for more
      details.
    * __--idlink__ URL tempate for information link for VCF ID values. The token $$ will be substituted with the ID
      value. Example: ```--idlink 'https://www.ncbi.nlm.nih.gov/snp/?term=$$'```
    * __--no-embed__ Don't embed data. Fasta and track URLs are referenced unchanged. The resulting report is dependent
      on the original data files, which must be specified as URLs. Local files are not supported with this option.
    * __--subsample__ FLOAT. Output only a portion of input alignments (0.0 -> 1.0). See `samtools view` documentation
      for more details
    * __--maxlen__ INT. Maximum length of a variant (SV) to show in a single view. Variants exceeding this length will
      be shown in a split-screen (multilocus) view. default = 10000
    * __--translate-sequence-track__ Three-frame Translate sequence track
    * __--tabulator__ Use the tabulator template for the table
    * __--filter-config__ YAML config file for column setup for tabulator.
    * __--merge-overlaps__ Merge overlapping intervals in multi-locus files such as bedpe. If set bedpe features with
      overlapping regions will be presented in a single locus view. Default is false.
    * __--title__ STRING. Title for the report. Default is "IGV Report".
    * __--header__ STRING. Path to a HTML file to be included in the report.  The header file content will be included
      directly after the `<body>` tag in the report HTML file.
    * __--footer__ STRING. Path to a HTML file to be included in the report. The footer file content will be included
      directly before the `</body>` tag in the report HTML file.

**Track file formats:**

Currently supported track file formats are BAM, CRAM, VCF, BED, GFF3, GTF, WIG, and BEDGRAPH. FASTA. BAM, CRAM, and
VCF files must be indexed. Tabix is supported and it is recommended that all large files be indexed.

**Example**

The script below creates a variant report from a VCF file and an alignment (BAM) file.  Five info fields from the VCF
are specified for inclusion in the variant table. The report is created for the hg38 genome and given a custom title.

```bash

create_report test/data/variants/variants.vcf.gz \
--genome hg38 \
--info-columns GENE TISSUE TUMOR COSMIC_ID GENE SOMATIC \
--tracks test/data/variants/variants.vcf.gz test/data/variants/recalibrated.bam \
--title "IGV Variant Inspector"
--output example_vcf.html

```

See the [examples page](https://igvteam.github.io/igv-reports/) for more examples.

`

#### Converting genomic files to data URIs for use in igv.js

The script ```create_datauri``` (```python igv_reports/datauri.py```) converts the contents of a file to a data uri for
use in igv.js. The datauri will be printed to stdout.  *NOTE* It is not neccessary to run this script explicitly to
create a report, it is documented here
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
