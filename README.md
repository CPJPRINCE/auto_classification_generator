# Auto Classification Generator Tool


It is compatible with Windows, MacOS and Linux operating systems (though testing has been limited on MacOS).

## What does this tool do?

This tool will recusrively generater classification codes, following an ISAD(G) convention, for a given directory / folder to an Excel or CSV spreadsheet.

## Why use this tool?

If you're an archivist dealing with Digital Records, this provides a means of undertaking a classification of hundreds and and thousands of records, saving a significant amount of time on large projects. This tool can also be hooked into python scripts, see my other Opex Manifest Generator project.

## Additional features:

- Appendable prefix.
- Changable starting reference.
- Logged removal of empty directories.
- Alternative "accession reference" mode.
- Compatiable with Win32 / 256 Character Limit.

## Why not use this tool

The classification will generate an archival reference code for each file, down to item level. If you're institution does not classify Digital records down to item level, this is not a suitable tool for you. At the moment, the program cannot group together higher levels. To note there can extraneously long classification codes, depending on the depth of the folders.


## Sturcture of References

Folder                  Reference
-->Root                 0
---->Folder 1           0/1
------>Sub Folder 1     0/1/1
-------->File 1         0/1/1/1
-------->File 2         0/1/1/2
------>Sub Folder 2     0/1/2
-------->File 3         0/1/2/1
-------->File 4         0/1/2/2
---->Folder 2           0/2
------>Sub Folder 3     0/2/1

The root reference defaults to 0, however this the Prefix option can be utilised to change 0 to the desired prefix / archival reference: 

--prefix "ARC"

Changes:

-->Root Folder          ARC
---->Folder             ARC/1
------>Sub Folder       ARC/1/1
etc

## Prerequisites

The following modules are utilised and installed with the package:
- pandas
- openpyxl

Python Version 3.8+ is also recommended. It may work on earlier versions, but this has not been tested.

## Installation

To install simply run:

`pip install auto_classification_generator`

## Usage

To run the basic program, run from the terminal:

`auto_classification_generator {path/to/your/folder}`

Replacing the path with your folder. If a space is in the path enclose in quoations. On Windows this may look like:

`auto_classification_generator "C:\Users\Christopher\Downloads\"`

To run the program with the Prefix options enabled:

`auto_classification_generator "C:\Users\Christopher\Downloads\"` -p "MyDownloads"

## Options:

The following options are currently avilable to run the program with:

```
Options:
        -h,     --help          Show Help dialog
        -p,     --prefix        Replace Root 0 with specified prefix    [string]
        -acc,   -accession      Run in "Accession Mode", this will generate a running number of either Files, Directories or Both {None,Dir,File,All}
        -accp,  --acc-prefix    Set the Prefix to append onto the running number generated in "Accession Mode"
        -s,     --start-ref     Set the Reference to start from.        [int]
        -o,     --output        Set the directory to export      
        -m,     --meta-dir      Set whether to generate a "meta" directory, to export CSV / Excel file to. Default behaviour will be to create a directory, using this option will disable it.         [boolean]
        --skip                  Skip running the Auto Classification process, will generate a spreadsheet but not an Archival Reference [boolean]
        -fmt,   --format        Set whether to export as a CSV or XLSX file.
```