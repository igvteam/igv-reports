# igv.js-reports

Python application to generate dataURIs from genomic data files and self-contained igv.js pages that can
be opened within a browser with "file" protocol.

**_Requires Python 3.  Tested with Python 3.4.6._**

## Installation
First install all requirements.
```sh
pip install -r requirements.txt
```

## Converting a genomic data file to an igv.js Data URI

If you just want to get a data URI that can be read by igv.js in place of a url to a data file, use the get_datauri.py script
```sh
python get_datauri.py [filename]
```
The data uri will be printed to stdout.


## Creating a fusion inspector report from an existing html file

Note: These instructions are specifically for Fusion Inspector 
reports.  See [https://github.com/FusionInspector/FusionInspector/wiki](https://github.com/FusionInspector/FusionInspector/wiki)


First make sure that the file contains the comment line `<!-- start igv report here -->` within a script tag.
Directly below this line a javscript variable called "data" will be created so insure that no other variable names conflict.  
  
Then use the create_fusion_report.py script to create a new self-contained html file.
```sh
python create_fusion_report.py [filename]
```
where filename is the path to the igv.js html template file.  Refer to example/FI_viewer/igvjs_fusion_viewer.html for an example.

```sh
python create_report.py example/FI_viewer/igvjs_viewer.html
```

After, running the script, see example/FI_viewer/igvjs_fusion_viewer_report.html for the result.

