# Auto Classification Generator Tool

The Auto-classification tool is small python programme to help Digital archivists classify and catalogue Digital Items. It recursively acts through a given directory to create generating an ISAD(G) classification code for each directory and file, then exporting the results to an Excel or CSV spreadsheet.

It's platform independent tested functioning on Windows, MacOS and Linux. 

## Why use this tool?

If you're an archivist dealing with Digital Records, this provides a means of undertaking a classification of hundreds and and thousands of records, saving a significant amount of time on when dealing with large amounts of records.

Arrangement can be done before generation of the spreadsheet.

For developer's, this tool can also be hooked into python scripts.

## Additional features:

Some additional features include.

- Append prefixes to the Archival Reference.
- Identifying the depth of each folder.
- Gathering standard set of Metadata.
- Changeable starting reference.
- Logged removal of empty directories.
- An alternative "Accession Reference" mode.
- Compatibility with Win32 / Window's 256 Character limit.

## Why not use this tool?

The classification will generate an archival reference code for each file, down to item level. If you're institution does not classify Digital records down to item level, this is not a suitable tool for you. At the moment, the program cannot group together higher levels. There can also extraneously long classification codes, depending on the depth of the folders.

This tool might still be of be helpful as it can identify the depth of the folders. Alternatively the spreadsheet's template is also the basis of the template used in my "Opex Manifest Generator" tool *\*Shameless Self promotion\**.

## Structure of References
```
Folder                  Reference
-->Root                 0
---->Folder 1           1
------>Sub Folder 1     1/1
-------->File 1         1/1/1
-------->File 2         1/1/2
------>Sub Folder 2     1/2
-------->File 3         1/2/1
-------->File 4         1/2/2
---->Folder 2           2
------>Sub Folder 3     2/1
```
The root reference defaults to 0, however this the Prefix option can be utilized to change 0 to the desired prefix / archival reference, changing the structure to:

```
-->Root Folder          ARC
---->Folder             ARC/1
------>Sub Folder       ARC/1/1
etc
```

## Prerequisites

The following modules are utilized and installed with the package:
- pandas
- openpyxl

Python Version 3.8+ is also recommended. It may work on earlier versions, but this has not been tested.

## Installation

To install, simply run:

`pip install -U auto_classification_generator`

## Usage

To run the basic program, run from the terminal:

`auto_class {path/to/your/folder}`

Replacing the path with your folder. If a space is in the path enclose in quotations. On Windows this may look like:

`auto_class "C:\Users\Christopher\Downloads\"`

Additional options can be appended before or after the root directory is given. For instance, to run the program with the Prefix set to "MyDownloads", you can run:

`auto_class "C:\Users\Christopher\Downloads\" -p "MyDownloads"`


## Options:

The following options are currently available to run the program with:

```
Options:
        -h,     --help          Show Help dialog                              
        -p,     --prefix        Replace Root 0 with specified prefix            [string]
        -acc,   -accession      Run in "Accession Mode", this will              {None,Dir,File,All}           
                                generate a running number of either Files, 
                                Directories or Both {None,Dir,File,All}
        -accp,  --acc-prefix    Set the Prefix to append onto the running       [boolean]
                                number generated in "Accession Mode"
        -rm     --empty         Will remove all Empty Directories from          [boolean]
                                within a given folder, not including them
                                in the Reference Generation.
                                A simply Text list of removed folders is 
                                then generated to the output directory.
        -s,     --start-ref     Set the number to start the Reference           [int] 
                                generation from.
        -o,     --output        Set the directory to export the spreadsheet to. [string]      
        -m,     --meta-dir      Set whether to generate a "meta" directory,     [boolean]
                                to export CSV / Excel file to.
                                Default behavior will be to create a directory,
                                using this option will disable it.      
                --skip          Skip running the Auto Classification process,   [boolean]
                                will generate a spreadsheet but not
                                an Archival Reference
        -fmt,   --format        Set whether to export as a CSV or XLSX file.    {csv,xlsx}
                                Otherwise defaults to xlsx.
```

## Future Developments

- Level Limitations to allow for "group references".
- Generating reference's which use alphabetic characters...

## Contributing

I welcome further contributions and feedback.
