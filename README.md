# Auto Classification Generator
This software is intended for use in Digital Archiving, to generate classification tree's based directly on a directory hierachy.

**What does this do?**

It will generate an Excel spreadsheet containing a generated archival reference / classification code for folders and files, alongside a directory listing. Each folder is considered a level and each file an item, on each new folder a new level is made.

**Why use this tool**

If you're an archivist dealing with Digital Records, this provides a means of undertaking a classification of hundreds and and thousands of records, saving a significant amount of time on large projects. This tool can also be hooked into python scripts, see my other Opex Manifest Generator project.

Additional features:
  + Appendable prefix.
  + Changable starting reference.
  + Logged removal of empty directories.
  + Alternative "accession reference" mode.
  + Compatiable with Win32 / 256 Character Limit.

**Why not use this tool**

The classification will generate an archival reference code for each file, down to item level. If you're institution does not classify Digital records down to item level, this is not a suitable tool for you. At the moment, the program cannot group together higher levels. To note there can extraneously long classification codes, depending on the depth of the folders.

**Prequisites**

The software is compatiable with Windows, Mac (untested) and Linux platforms.
You will need Python 3.8+ and the following modules;
+ pandas
+ pathlib
+ lxml

You can run this, to install all necessary modules:
`pip install pandas pathlib lxml`

**Running the program**

To run the program, clone the repo to a directory, open that directory in a command line program and run.

`   git clone https://github.com/CPJPRINCE/auto_classification_generator.git    
    cd .\auto_classification_generator    
python .\auto_classiciation_generator.py \path\to\folder`

Replacing `\path\to\folder` with a real path.

This will create a `meta` directory, within the above, which contianing a spreadsheet: `Folder_AutoClass.xlsx`

In the spreadsheet...
