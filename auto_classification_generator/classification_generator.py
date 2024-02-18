"""
Auto Classification Generator tool

This tool is utilised to recusrively generater classification codes, following an ISAD(G) convention, for a given directory / folder to an Excel or CSV spreadsheet.

It is compatible with Windows, MacOS and Linux Operating Systems.

author: Christopher Prince
license: Apache License 2.0"
"""

from auto_classification_generator.common import *
import os
import pandas as pd
from datetime import datetime
import time
import argparse

class ClassificationGenerator():
    def __init__(self,
                 root,
                 output_path=os.getcwd(),
                 prefix=None,
                 accprefix=None,
                 start_ref=1,
                 empty_flag=False,
                 skip_flag=False,
                 accession_flag=None,
                 meta_dir_flag=True,
                 output_format="xlsx"):
        
        self.root = os.path.abspath(root)
        self.root_level = self.root.count(os.sep)
        self.root_path = os.path.dirname(self.root)         
        self.output_path = output_path
        self.output_format = output_format
        self.empty_flag = empty_flag
        self.skip_flag = skip_flag
        self.prefix = prefix
        self.start_ref = int(start_ref)
        self.reference_list = []
        self.record_list = []
        self.accession_flag = accession_flag
        self.accession_list = []
        self.accession_count = start_ref
        if accprefix: self.accession_prefix = accprefix
        else: self.accession_prefix = prefix
        self.empty_list = []
        self.meta_dir_flag = meta_dir_flag
    
    def remove_empty_directories(self):
        """
        Remove's empty directories with a warning.
        """
        confirm_delete = input('\n***WARNING*** \
                               \n\nYou have selected the Remove Empty Folder\'s Option. \
                               \nThis process is NOT reversible! \
                               \n\nPlease confirm this by typing in "Y" \
                               \nTyping in any other character will cause this program to self destruct... \
                               \n\nPlease confirm your choice: ')
        if not confirm_delete in {"Y","y"}:
            print('Running self destruct program...\n')
            for n in reversed(range(10)):
                print(f'Self destruction in: {n}',end="\r")
                time.sleep(1)
                raise SystemExit()
        walk = list(os.walk(self.root))
        for path, _, _ in walk[::-1]:
            if len(os.listdir(path)) == 0:
                self.empty_list.append(path)
                os.rmdir(path)
                print(f'Removed Directory: {path}')
        if self.empty_list: 
            output_txt = define_output_file(self.output_path,self.root,self.meta_dir_flag,output_suffix="_EmptyDirectoriesRemoved",output_format="txt")
            export_list_txt(self.empty_list, output_txt)
        else: print('No directories removed!')

    def filter_directories(self,directory):
        """Sorts the list Alphabetically and filters out certain files.
        
        Currently hardcoded to ignore:
        1. Hidden Directories starting with '.'
        2. '.opex' files
        3. Folders titled 'meta'
        4. Script file
        5. Output file
        
        Look to make dynamic and customisable...
        """ 
        list_directories = sorted([f for f in os.listdir(directory) \
            if not f.startswith('.') \
            and not f.endswith('.opex') \
            and f != 'meta'\
            and f != os.path.basename(__file__) \
            and not f.endswith(f'_AutoClass.{self.output_format}') and not f.endswith(f'_autoclass.{self.output_format}')\
            and not f.endswith('_EmptyDirectoriesRemoved.txt')],key=str.casefold)
        return list_directories
    
    def parse_directory_dict(self,file_path,level,ref):
        """
        Parse's directory / file data into a dict which is then appened to a list
        """
        full_path = os.path.abspath(file_path)
        file_stats = os.stat(file_path)                               
        if self.accession_flag:                                                   
            acc_ref = self.accession_running_number(file_path)
            self.accession_list.append(acc_ref)
        if os.path.isdir(file_path): file_type = "Dir"
        else: file_type = "File"
        class_dict = {'RelativeName': str(file_path).replace(self.root_path,""),
                        'FullName':str(full_path),
                        'Basename': os.path.splitext(os.path.basename(file_path))[0],
                        'Extension': os.path.splitext(file_path)[1],
                        #'Parent':str(Path(full_path).parent),
                        'Parent': os.path.abspath(os.path.join(full_path, os.pardir)), # Alt Parent 
                        'Attribute':file_type,
                        'Size':file_stats.st_size,
                        'CreateDate':datetime.fromtimestamp(file_stats.st_ctime),
                        'ModifiedDate': datetime.fromtimestamp(file_stats.st_mtime),
                        'AccessDate':datetime.fromtimestamp(file_stats.st_atime),
                        'Level':level,
                        'Ref_Section':ref}
        self.record_list.append(class_dict)
        return class_dict
        
    def list_directories(self,directory,ref=1):
        """
        Generates a list of directories. Also calculate's level and a running reference number.
        """
        ref = int(ref)
        try:
            list_directory = self.filter_directories(directory)
            level = directory.count(os.sep) - self.root_level + 1 # Counts the number of Seperators in the current file and subtracts from rootlevels (giving current level).
            for file in list_directory:
                file_path = os.path.join(directory,file)        
                # Processing and appending the metadata to lists.
                self.parse_directory_dict(file_path,level,ref)
                ref = int(ref) + int(1)
                if os.path.isdir(file_path): self.list_directories(file_path,ref=1)
        except Exception as e:
            print(e)
            print("Error Occured for directory/file: {}".format(list_directory))
            pass
        
    def init_dataframe(self):
        """
        The directories are listed which are listed and form dicts from above two functions.
        This looks up and pulls through the Parent row's data to the Child Row.
        The dataframe is merged on itself, Parent is merged 'left' on FullName to pull through the Parent's data (lookup is based on File Path's), and unnecessary data is dropped.
        Any errors are turned to 0 and the result are based to the reference loop init. 
        """
        self.parse_directory_dict(file_path=self.root,level=0,ref=0)
        self.list_directories(self.root,self.start_ref) # Lists Directories..
        df = pd.DataFrame(self.record_list)                                                                            
        df = df.merge(df[['FullName','Ref_Section']],how='left',left_on='Parent',right_on='FullName')              
        df = df.drop(['FullName_y'], axis=1)                                                                            
        df = df.rename(columns={'Ref_Section_x':'Ref_Section','Ref_Section_y':'Parent_Ref','FullName_x':'FullName'})    # Rename occurs to realign columns
        df['Parent_Ref'] = df['Parent_Ref'].fillna(0)                                                                   # Any Blank rows in Parent Ref set to 0                                                      
        df = df.astype({'Parent_Ref': int})                                                                             # Parent Ref is set as Type int
        df.index.name = "Index"
        self.list_loop = df[['Ref_Section','Parent','Level']].values.tolist()                                           # Reference Section, Parent and Levels are exported to lists for iterating in ref_loop
        self.df = df
        if self.skip_flag: pass
        else: self.init_reference_loop()
        return self.df
    
    def init_reference_loop(self):
        """
        Intiation of the Reference loop. Sets some of the prevariables necessary for the loop.
        """
        c = 0                       
        tot = len(self.list_loop)
        #print(tot)
        for REF,PARENT,LEVEL in self.list_loop:
            #print(REF,PARENT,LEVEL)
            c += 1
            print(f"Generating Auto Classification for: {c} / {tot}",end="\r") # For a simple progress bar....
            TRACK = 1  
            self.reference_loop(REF,PARENT,TRACK,LEVEL)  #Start's Reference Loop - Recursive Function, so operates on it's own!
        print()
        self.df['Archive_Reference'] = self.reference_list
        if self.accession_flag:
            self.df['Accession_Reference'] = self.accession_list
        return self.df
    
    def reference_loop(self, REF, PARENT, TRACK, LEVEL, NEWREF=None):
        """
        Note that the Reference loop is acting inside the for loop of the init step.

        REF is the reference section derived from the list in the list_directories function. [Stay's Constant]
        PARENT is the parent folder of the child. [Vary's]
        TRACK is an iteration tracker to distinguish between first and later iterations. [Vary's]
        LEVEL is the level of the folder, 0 being the root. [Stay's Constant]

        NEWREF is the important variable here and is archive reference constructed during this loop.

        To do this the reference loop works upwards, running an "index lookup" against the parent folder until it reaches the top.
        
        1) To start, the reference loop indexes from the dataframe established by listing the directories.
        2) The index compares FullName against the Parent (So acting on the Basis of File Path's)
        3) If the index fails / is 0, then the top has been reached.
        4) In that event if LEVEL is also 0 IE the top-most item is being looked at (normally the first thing). NEWREF is set to REF
        5) Otherwise the top-most level has been reached and, NEWREF is simply NEWREF.
        6) If the index does matches, then top level has not yet been reached. In this case we also account for the PARENT's Reference, to avoid an error at the 2nd to top layer.
        7) PARENTREF is looked up, by Indexing the Dataframe. Then if PARENTREF is 0, IE we're on the 2nd top layer. We check the TRACK.
        8) If TRACK is 1, IE the first iteration on the 2nd layer, NEWREF is just REF.
        9) If TRACK isn't 1, IE subsquent iteration's on the 2nd layer, NEWREF is just itself.
        10) If PARENTREF isn't 0, then we concatenate the PARENTREF with either REF or NEWREF.
        11) If TRACK is 1, NEWREF is PARENTREF + REF.
        12) If TRACK isn't 1, NEWREF is PARENTREF + NEWREF.

        13) At the end of the process the PARENT of the current folder is looked up and SUBPARENT replace's the PARENT variable. TRACK is also advanced.
        14) Then function is then called on recusrively. In this way the loop will work through until it reaches the top. 
        15) this is only called upon if the index does not fail. If it does fail, then the top-level is reached and the loop escaped.
        16) As this is acting within the Loop from the init stage, this will operate on all files within a list.
        """
        try:
            idx = self.df.index[self.df['FullName'] == PARENT]
            if idx.size == 0:
                if LEVEL == 0:
                    NEWREF = str(REF)
                    if self.prefix: NEWREF = str(self.prefix)
                else:
                    NEWREF = str(NEWREF)
                    if self.prefix: NEWREF = str(self.prefix) + "/" + str(NEWREF)
                self.reference_list.append(NEWREF)
            else:
                PARENTREF = self.df.loc[idx].Ref_Section.item() 
                if PARENTREF == 0:
                    if TRACK == 1: NEWREF = str(REF)            
                    else: NEWREF = str(NEWREF)                       
                else:
                    if TRACK == 1: NEWREF = str(PARENTREF) + "/" + str(REF)         
                    else: NEWREF = str(PARENTREF) + "/" + str(NEWREF)              
                    
                SUBPARENT = self.df.loc[idx].Parent.item() 
                PARENT = SUBPARENT
                TRACK = TRACK+1
                self.reference_loop(REF, PARENT, TRACK, LEVEL, NEWREF)

        except Exception as e:
            print('Passed?')
            print(e)
            pass 

    def accession_running_number(self,file_path):
        if self.accession_flag == "File":
            if os.path.isdir(file_path): accession_ref = self.accession_prefix + "-Dir"
            else: accession_ref = accession_ref = self.accession_prefix + "-" + str(self.accession_count); self.accession_count += 1
        elif self.accession_flag == "Dir":
            if os.path.isdir(file_path): accession_ref = self.accession_prefix + "-" + str(self.accession_count); self.accession_count += 1
            else: accession_ref = accession_ref = self.accession_prefix + "-File"
        elif self.accession_flag == "All":
            accession_ref = self.accession_prefix + "-" + str(self.accession_count); self.accession_count += 1
        return accession_ref
            
    def main(self):
        if self.empty_flag: self.remove_empty_directories()
        self.init_dataframe()
        output_file = define_output_file(self.output_path,self.root,meta_dir_flag=self.meta_dir_flag,output_format=self.output_format)
        if self.output_format == "xlsx": export_xl(df=self.df,output_filename=output_file)
        elif self.output_format == "csv": export_csv(df=self.df,output_filename=output_file)

def parse_args():
    parser = argparse.ArgumentParser(description="OPEX Manifest Generator for Preservica Uploads")
    parser.add_argument('rootpath',nargs='?', default=os.getcwd())
    parser.add_argument("-p","--prefix",required=False, nargs='?')
    parser.add_argument("-accp", "--acc-prefix",required=False, nargs='?')
    parser.add_argument("-rm","--empty",required=False,action='store_true')
    parser.add_argument("-acc","--accession",required=False,choices=['None','Dir','File','All'],default=None)
    parser.add_argument("-o","--output",required=False,nargs='?')
    parser.add_argument("-s","--start-ref",required=False,nargs='?',default=1)
    parser.add_argument("-m","--meta-dir",required=False,action='store_true',default=True)
    parser.add_argument("--skip",required=False,action='store_true',default=False)
    parser.add_argument("-fmt","--output-format",required=False,default="xlsx",choices=['xlsx','csv'])
    
    args = parser.parse_args()
    return args


def cli():
    args = parse_args()
    if isinstance(args.rootpath,str): args.rootpath = args.rootpath.strip("\"").rstrip("\\")
    if not args.output:
        args.output = os.path.abspath(args.rootpath)
        print(f'No output path selected, defaulting to root Directory: {args.output}')
    else:
        args.output = os.path.abspath(args.output)
        print(f'Output path set to: {args.output}')
        
    ClassificationGenerator(args.rootpath,
                            output_path=args.output,
                            prefix=args.prefix,
                            accprefix=args.acc_prefix,
                            empty_flag=args.empty,
                            accession_flag=args.accession,
                            start_ref=args.start_ref,
                            meta_dir_flag=args.meta_dir,
                            skip_flag=args.skip,
                            output_format=args.output_format).main()
    print('Complete!')