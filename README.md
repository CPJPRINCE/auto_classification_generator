# Auto Classification Generator Tool

The Auto-classification tool is small python programme to help Digital archivists classify and catalogue Digital Items. It recursively acts through a given directory to create generating reference codes for each directory and file, then exporting the results to an Excel or CSV spreadsheet.

It's platform independent tested functioning on Windows, MacOS and Linux. 

## Why use this tool?

If you're an archivist dealing with Digital Records, this provides a means of undertaking a classification of numerous records at a time, saving a significant amount of time in assigning reference codes to individual records.

The generated spreadsheet also serves as the basis for spreadsheet inputs for the Opex Manifest Generator tool [*\*Shameless Self promotion\**.](https://github.com/CPJPRINCE/opex_manifest_generator/)

## A Quick Note

If you need to conduct an arrangement of the files; this must be done beforehand for the references to be accurate; though a temporary spreadsheet can be generated to provide assistance in this.

## Additional features:

Some additional features include.

- Append prefixes to the Archival Reference.
- Identifying the depth / level of each folder.
- Gathering standard set of Metadata.
- Changeable starting reference.
- Logged removal of empty directories.
- An alternative "Accession Reference" mode.
- Compatibility with Win32 / Window's 256 Character limit.

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
------>File 5           2/2
---->File 6             3
```
The root reference defaults to 0, however this the Prefix option can be utilized to change 0 to the desired prefix / archival reference, changing the structure to:

```
-->Root Folder          ARC
---->Folder             ARC/1
------>Sub Folder       ARC/1/1
------>File             ARC/1/2
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

Additional options can be appended before or after the root directory.

To run the program with the Prefix option, add the `-p` option and type in your prefix:

`auto_class "C:\Users\Christopher\Downloads\" -p "ARCH"`

This will generate a spreadsheet in a folder called 'meta' within the 'root' directory.

![MetaFolder](assets/metaFolder.png)

The spreadsheet will be named after the 'root' folder and appended with "_AutoClass".

![FolderSpread](assets/SpreadGen.png)

Within the spreadsheet you will have information on the paths of the files as well as some additional metadata: size, extensions and dates. 

![SpreadPreview](assets/SpreadPreview.png)

At the end of the spreadsheet an `Archive_Reference` column with the generated refrence. 

![ReferencePreview](assets/ReferencesPreview.png)

(If ran without Prefix Option this will simply be the numerals)

## Accession mode

There is an alternative method of generating a reference number; having create a code based on the directory hierachy you can simply create one that follows an 'accession number' pattern. IE each file or folder regardless of depth will be given a running number; depending on the 'mode' the running number will only apply to Directories, Files or Both!


```
Example running Accession in "File" Mode

----> Root              ACC-Dir
------> Folder 1        ACC-Dir
--------> File 1        ACC-1
--------> File 2        ACC-2
------> File 3          ACC-3
------> Folder 2        ACC-Dir
--------> Sub-Folder    ACC-Dir
----------> File 4      ACC-4
```

The available modes are `File, Dir, All`

To run in accession mode, use the `-acc` and `-accp` options (A prefix must be set):

`auto_class "C:\Users\Christopher\Downloads\" -acc File -accp "ACC"`

![AccessionPReview](assets/AccessionPreview.png)

When you generate an Accession Reference an Archive_Reference code will always also be generated.

## Set start reference

To set a start reference simply add `-s` followed by (Note this must be numeral)

## Clear Empty Directories

Adding `--empty` or `-rm` to the will automatically remove any empty directories within the files. It will also generate a simple text log in the meta folder of the empty directories that were removed.

## Fixity

You can also generate Fixities by simply adding the `-fx` option. This will default to using the SHA-1 algorithm, only MD5, SHA-1, SHA-256 and SHA-512 are supported. 

![HashPreview](assets/HashPreview.png)

To run a SHA-512 generation:

`auto_class "C:\Users\Christopher\Downloads\" -fx SHA-512`

## Filtering

By default hidden folders and folders named 'meta' will be ignored. You can include hidden folders by using the option `--hidden`

## Skip

If you just want to generate a spreadsheet without a reference code you can add `--skip`, and it will gsimply generate a spreadsheet without the Archive_Reference

## Options:

The following options are currently available to run the program with:

```
Options:
        -h,     --help          Show Help dialog                              
        -p,     --prefix        Replace Root 0 with specified prefix            [string]
        
        -acc,   -accession      Run in "Accession Mode", this will              {None,Dir,File,
                                                                                All}           
                                generate a running number of either Files, 
                                Directories or Both {None,Dir,File,All}
        -accp,  --acc-prefix    Set the Prefix to append onto the running       [boolean]
                                number generated in "Accession Mode"
        
        -fx     --fixity        Generate fixity codes for files                 {MD5, SHA-1, 
                                                                                SHA-256, SHA-512}
        
        --hidden                Include Hidden directories and files in         [boolean]
                                generation.

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
        
        --skip                  Skip running the Auto Classification process,   [boolean]
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
