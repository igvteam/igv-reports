# igv.js-reports
Python application to generate self-contained igv.js pages that can be opened with in a browser with "file" protocol.

## Installation
First install all requirements.
```sh
pip install -r requirements.txt
```
## Creating a report from an existing html file
First make sure that the file contains the comment line `<!-- start igv report here -->` within a script tag.
Directly below this line a javscript variable called "data" will be created so ensure that no other variable names conflict.  
  
Then use the create_report.py script to create a new self-contained html file.
```sh
python create_report.py [filename]
```
where filename is the path to the igv.js html file.  

Refer to example/FI_viewer/igvjs_viewer.html for an example.
```sh
python create_report.py example/FI_viewer/igvjs_viewer.html
```
After, running the script, see example/FI_viewer/igvjs_viewer_report.html for the result.

### Getting a Data Uri
If you just want to get a data URI that can be read by igv.js in place of a url, use the get_datauri.py script
```sh
python get_datauri.py [filename]
```
The data uri will be printed to stdout.