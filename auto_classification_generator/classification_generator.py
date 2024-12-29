"""
Auto Classification Generator tool

This tool is utilised to recusrively generater classification codes, following an ISAD(G) convention, for a given directory / folder to an Excel or CSV spreadsheet.

It is compatible with Windows, MacOS and Linux Operating Systems.

author: Christopher Prince
license: Apache License 2.0"
"""

from auto_classification_generator.common import *
from auto_classification_generator.hash import *
import os, time, datetime
import pandas as pd
import configparser

class ClassificationGenerator():
    """
    A Tool for generating archival references for any given directory for use by Digital Archivists.
    Will turn the hierachy of a folder into and return the results as spreadsheet (or other output).

    :param root: the directory to generate references for
    :param output_path: set the output path
    :param prefix: set a prefix to append to generated references
    :param accprefix: set a prefix to append to generated accession references
    :param start_ref: set the starting reference, only affects first instance
    :param fixity: set whether to generate fixites
    :param empty_flag: set whether to delete and log empty directories
    :param skip_flag: set whether to skip reference generation (outputs set data)
    :param accession_flag: set whether to generate accession reference (running number)
    :param meta_dir_flag: set whether to generate a 'meta' dir for output
    :param hidden_flag: set to include hidden files/directories
    :param output_format: set to specify output format [xlsx, csv, ods, xml, json, dict] are supported, may require additional modules.
    :param delimiter: set delimiter for generated references
    :param keywords: set to replace numbers in reference with alphabetical characters, specified in list
    :param keywords_mode: set to specify keywords mode [intialise, firstletters] 
    :param keywords_retain_order: set to continue counting reference, if keyword is used, skips numbers if not
    :param sort_key: set the sort key, can be any valid function for sorted
    :param keywords_abbreviation: set int for number of characters to abbreviate to for keywords mode
    :param options_file: set an options file to adjust field parameters
    """
    def __init__(self, 
                 root: str, 
                 output_path: str = os.getcwd(), 
                 prefix: str = None, 
                 accprefix: str = None, 
                 start_ref: int = 1, 
                 fixity: str = None, 
                 empty_flag: bool = False, 
                 skip_flag: bool = False, 
                 accession_flag: bool = False, 
                 meta_dir_flag: bool = True, 
                 hidden_flag: bool = False, 
                 output_format: str = "xlsx",
                 delimiter: str = "/",
                 keywords: list = None,
                 keywords_mode: str = "intialise",
                 keywords_retain_order: bool = False,
                 sort_key = lambda x: (os.path.isfile(x), str.casefold(x)),
                 keywords_abbreviation_number: int = None,
                 options_file: str = os.path.join(os.path.dirname(__file__),'options.properties')):

        self.root = os.path.abspath(root)
        self.root_level = self.root.count(os.sep)
        self.root_path = os.path.dirname(self.root)
        self.output_path = output_path
        self.output_format = output_format
        self.prefix = prefix
        self.start_ref = start_ref
        self.fixity = fixity
        self.delimiter = delimiter
        if self.delimiter is None:
            self.delimiter_flag = False
        else:
            self.delimiter_flag = True
        self.keyword_list = keywords
        self.keywords_mode = keywords_mode
        self.keywords_retain_order = keywords_retain_order
        self.sort_key = sort_key
        self.keywords_abbreviation_number = keywords_abbreviation_number

        self.accession_count = start_ref
        if accprefix:
            self.accession_prefix = accprefix
        else:
            self.accession_prefix = prefix

        self.reference_list = []
        self.record_list = []
        self.empty_list = []
        self.accession_list = []

        self.meta_dir_flag = meta_dir_flag
        self.accession_flag = accession_flag
        self.empty_flag = empty_flag
        self.skip_flag = skip_flag
        self.hidden_flag = hidden_flag

        self.parse_config(options_file=os.path.abspath(options_file))
        self.start_time = datetime.datetime.now()

    def parse_config(self, options_file: str = 'options.properties'):
        config = configparser.ConfigParser()
        config.read(options_file, encoding='utf-8')
        global INDEX_FIELD
        INDEX_FIELD = config['options']['INDEX_FIELD']
        global PATH_FIELD
        PATH_FIELD = config['options']['PATH_FIELD']
        global RELATIVE_FIELD
        RELATIVE_FIELD = config['options']['RELATIVE_FIELD']
        global PARENT_FIELD
        PARENT_FIELD = config['options']['PARENT_FIELD']
        global PARENT_REF
        PARENT_REF = config['options']['PARENT_REF']
        global REFERENCE_FIELD
        REFERENCE_FIELD = config['options']['REFERENCE_FIELD']
        global ACCESSION_FIELD
        ACCESSION_FIELD = config['options']['ACCESSION_FIELD']
        global REF_SECTION
        REF_SECTION = config['options']['REF_SECTION']
        global LEVEL_FIELD
        LEVEL_FIELD = config['options']['LEVEL_FIELD']
        global BASENAME_FIELD
        BASENAME_FIELD = config['options']['BASENAME_FIELD']
        global EXTENSION_FIELD
        EXTENSION_FIELD = config['options']['EXTENSION_FIELD']
        global ATTRIBUTE_FIELD
        ATTRIBUTE_FIELD = config['options']['ATTRIBUTE_FIELD']
        global SIZE_FIELD
        SIZE_FIELD = config['options']['SIZE_FIELD']
        global CREATEDATE_FIELD
        CREATEDATE_FIELD = config['options']['CREATEDATE_FIELD']
        global MODDATE_FIELD
        MODDATE_FIELD = config['options']['MODDATE_FIELD']        
        global ACCESSDATE_FIELD
        ACCESSDATE_FIELD = config['options']['ACCESSDATE_FIELD']


    def remove_empty_directories(self):
        """
        Remove empty directories with a warning.
        """
        confirm_delete = input('\n***WARNING*** \
                               \n\nYou have selected the Remove Empty Folders Option. \
                               \nThis process is NOT reversible! \
                               \n\nPlease confirm this by typing: "Y" \
                               \nTyping any other character will abort the program... \
                               \n\nPlease confirm your choice: ')
        if confirm_delete.lower() != "y":
            print('Aborting...')
            time.sleep(1)
            raise SystemExit()
        empty_dirs = []
        for dirpath, dirnames, filenames in os.walk(self.root, topdown = False):
            if not any((dirnames, filenames)):
                empty_dirs.append(dirpath)
                try:
                    os.rmdir(dirpath)
                    print(f'Removed Directory: {dirpath}')
                except OSError as e:
                    print(f"Error removing directory '{dirpath}': {e}")
        if empty_dirs:
            output_txt = define_output_file(self.output_path, self.root, self.meta_dir_flag, 
                                            output_suffix = "_EmptyDirectoriesRemoved", output_format = "txt")
            export_list_txt(empty_dirs, output_txt)
        else:
            print('No directories removed!')

    def filter_directories(self, directory, sort_key = lambda x: (os.path.isfile(x), str.casefold(x))):
        """
        Sorts the list alphabetically and filters out certain files.
        """
        try:
            if self.hidden_flag is False:
                list_directories = sorted([win_256_check(os.path.join(directory, f.name)) for f in os.scandir(directory)
                                        if not f.name.startswith('.')
                                        and filter_win_hidden(win_256_check(os.path.join(directory, f.name))) is False
                                        and f.name != 'meta'
                                        and f.name != os.path.basename(__file__)],
                                        key = sort_key)
            elif self.hidden_flag is True:
                list_directories = sorted([os.path.join(directory, f.name) for f in os.scandir(directory) \
                                        if f.name != 'meta' \
                                        and f.name != os.path.basename(__file__)],
                                        key = sort_key)
            return list_directories
        except Exception:
            print('Failed to Filter')
            raise SystemError()

    def parse_directory_dict(self, file_path: str, level: str, ref: int):
        """
        Parses directory / file data into a dict which is then appended to a list
        """
        try:
            if file_path.startswith(u'\\\\?\\'):
                parse_path = file_path.replace(u'\\\\?\\', "")
            else: 
                parse_path = file_path
            file_stats = os.stat(file_path)
            if self.accession_flag:
                if self.delimiter_flag is False:
                    self.delimiter = "-"
                acc_ref = self.accession_running_number(parse_path, self.delimiter)
                self.accession_list.append(acc_ref)
            if os.path.isdir(file_path):
                file_type = "Dir"
            else:
                file_type = "File"
            class_dict = {
                        PATH_FIELD: str(os.path.abspath(parse_path)),
                        RELATIVE_FIELD: str(parse_path).replace(self.root_path, ""), 
                        BASENAME_FIELD: os.path.splitext(os.path.basename(file_path))[0], 
                        EXTENSION_FIELD: os.path.splitext(file_path)[1], 
                        PARENT_FIELD: os.path.abspath(os.path.join(os.path.abspath(parse_path), os.pardir)), 
                        ATTRIBUTE_FIELD: file_type, 
                        SIZE_FIELD: file_stats.st_size, 
                        CREATEDATE_FIELD: datetime.datetime.fromtimestamp(file_stats.st_ctime), 
                        MODDATE_FIELD: datetime.datetime.fromtimestamp(file_stats.st_mtime), 
                        ACCESSDATE_FIELD: datetime.datetime.fromtimestamp(file_stats.st_atime), 
                        LEVEL_FIELD: level, 
                        REF_SECTION: ref}
            if self.fixity and not os.path.isdir(file_path):
                hash = HashGenerator(self.fixity).hash_generator(file_path)
                class_dict.update({"Algorithm": self.fixity, "Hash": hash})
            self.record_list.append(class_dict)
            return class_dict
        except:
            print('Failed to Parse')
            raise SystemError()


    def list_directories(self, directory: str, ref: int = 1):
        """
        Generates a list of directories. Also calculates level and a running reference number.
        """
        ref = int(ref)
        pref = None
        try:
            list_directory = self.filter_directories(directory, sort_key = self.sort_key)
            if directory.startswith(u'\\\\?\\'):
                level = directory.replace(u'\\\\?\\', "").count(os.sep) - self.root_level + 1
            else:
                level = directory.count(os.sep) - self.root_level + 1
            for file_path in list_directory:
                file_name = win_file_split(file_path)
                if self.keyword_list is not None:
                    if len(self.keyword_list) == 0 and os.path.isdir(file_path):
                        if self.keywords_retain_order is False:
                            pref = ref - 1
                        elif self.keywords_retain_order is True:
                            pref = ref
                        ref = str(keyword_replace(file_name, mode=self.keywords_mode, abbreviation_number=self.keywords_abbreviation_number))
                    elif any(file_name in keyword for keyword in self.keyword_list) and os.path.isdir(file_path):
                        if self.keywords_retain_order is False:
                            pref = ref - 1
                        elif self.keywords_retain_order is True:
                            pref = ref
                        ref = str(keyword_replace(file_name, mode=self.keywords_mode, abbreviation_number=self.keywords_abbreviation_number))
                self.parse_directory_dict(file_path, level, ref)
                if pref:
                    ref = int(pref) + 1
                    pref = None
                else:
                    ref = int(ref) + 1
                if os.path.isdir(file_path):
                    self.list_directories(file_path, ref = 1)
        except Exception:
            print("Error occurred for directory/file: {}".format(list_directory))
            raise SystemError()

    def init_dataframe(self):
        """
        Lists the directories and forms dicts from the above two functions.
        Looks up and pulls through the Parent row's data to the Child Row.
        Merges the dataframe on itself, Parent is merged 'left' on FullName to pull through the Parent's data
        (lookup is based on File Path's), and unnecessary data is dropped.
        Any errors are turned to 0 and the result are based on the reference loop initialisation.
        """
        self.parse_directory_dict(file_path = self.root, level = 0, ref = 0)
        self.list_directories(self.root, self.start_ref)
        self.df = pd.DataFrame(self.record_list)
        self.df = self.df.merge(self.df[[INDEX_FIELD, REF_SECTION]], how = 'left', left_on = PARENT_FIELD, 
                                right_on = INDEX_FIELD)
        self.df = self.df.drop([f'{INDEX_FIELD}_y'], axis = 1)
        self.df = self.df.rename(columns = {f'{REF_SECTION}_x': REF_SECTION, f'{REF_SECTION}_y': PARENT_REF, 
                                          f'{INDEX_FIELD}_x': INDEX_FIELD})
        self.df[PARENT_REF] = self.df[PARENT_REF].fillna(0)
        self.df = self.df.astype({PARENT_REF: str})
        self.df.index.name = "Index"
        self.list_loop = self.df[[REF_SECTION, PARENT_FIELD, LEVEL_FIELD]].values.tolist()
        if self.skip_flag:
            pass
        else:
            self.init_reference_loop()
        return self.df

    def init_reference_loop(self):
        """
        Initialises the Reference loop. Sets some of the pre-variables necessary for the loop.
        """
        c = 0
        tot = len(self.list_loop)
        for ref, parent, level in self.list_loop:
            c += 1
            print(f"Generating Auto Classification for: {c} / {tot}", end = "\r")
            if self.delimiter_flag is False:
                self.delimiter = "/"
            self.reference_loop(ref = ref, parent = parent, track = 1, level = level, delimiter = self.delimiter)

        self.df[REFERENCE_FIELD] = self.reference_list
        if self.accession_flag:
            self.df[ACCESSION_FIELD] = self.accession_list
        return self.df

    def reference_loop(self, ref: str, parent: str, track: int, level: int, newref: str = None, delimiter: str = "/"):
        """
        The Reference loop works upwards, running an "index lookup" against the parent folder until it reaches the top.

        ref is the reference section derived from the list in the list_directories function. [Stays Constant]
        PARENT is the parent folder of the child. [Varies]
        TRACK is an iteration tracker to distinguish between first and later iterations. [Varies]
        LEVEL is the level of the folder, 0 being the root. [Stays Constant]

        newref is the archive reference constructed during this loop.

        To do this, the reference loop works upwards, running an "index lookup" against the parent folder until it reaches the top.
        1) To start, the reference loop indexes from the dataframe established by listing the directories.
        2) The index compares FullName against the Parent (So acting on the Basis of File Path's)
        3) If the index fails / is 0, then the top has been reached.
        4) In that event if LEVEL is also 0 IE the top-most item is being looked at (normally the first thing). newref is set to ref
        5) Otherwise the top-most level has been reached and, newref is simply newref.
        6) If the index does matches, then top level has not yet been reached. In this case we also account for the PARENT's Reference, to avoid an error at the 2nd to top layer.
        7) PARENTREF is looked up, by Indexing the Dataframe. Then if PARENTREF is 0, IE we're on the 2nd top layer. We check the TRACK.
        8) If TRACK is 1, IE the first iteration on the 2nd layer, newref is just ref.
        9) If TRACK isn't 1, IE subsequent iterations on the 2nd layer, newref is just itself.
        10) If PARENTREF isn't 0, then we concatenate the PARENTREF with either ref or newref.
        11) If TRACK is 1, newref is PARENTREF + ref.
        12) If TRACK isn't 1, newref is PARENTREF + newref.
        13) At the end of the process the PARENT of the current folder is looked up and SUBPARENT replace's the PARENT variable. TRACK is also advanced.
        14) Then the function is then called upon recursively. In this way the loop will work through until it reaches the top.
        15) This is only called upon if the index does not fail. If it does fail, then the top-level is reached and the loop escaped.
        16) As this is acting within the Loop from the init stage, this will operate on all files within a list.
        """
        try:
            idx = self.df[INDEX_FIELD][self.df[INDEX_FIELD] == parent].index
            if idx.size == 0:
                if level == 0:
                    newref = str(ref)
                    if self.prefix:
                        newref = str(self.prefix)
                else:
                    newref = str(newref)
                    if self.prefix:
                        newref = str(self.prefix) + delimiter + str(newref)
                self.reference_list.append(newref)
            else:
                parentref = self.df['Ref_Section'].loc[idx].item()
                if parentref == 0:
                    if track == 1:
                        newref = str(ref)
                    else:
                        newref = str(newref)
                else:
                    if track == 1:
                        newref = str(parentref) + delimiter + str(ref)
                    else:
                        newref = str(parentref) + delimiter + str(newref)
                parent = self.df['Parent'].loc[idx].item()
                track = track + 1
                self.reference_loop(ref, parent, track, level, newref, delimiter=delimiter)

        except Exception as e:
            print('Error in Reference Loop.')
            print(e)
            raise SystemError()
            pass

    def accession_running_number(self, file_path: str, delimiter: str = "-"):
        """
        Generates a Running Number / Accession Code, can be set to 3 different "modes", counting Files, Directories or Both
        """

        if self.accession_flag.lower() == "file":
            if os.path.isdir(file_path):
                if self.accession_prefix:
                    accession_ref = self.accession_prefix + delimiter + "Dir"
                else:
                    accession_ref = "Dir"
            else:
                if self.accession_prefix:
                    accession_ref = self.accession_prefix + delimiter + str(self.accession_count)
                else:
                    accession_ref = self.accession_count
                self.accession_count += 1
        elif self.accession_flag.lower() == "dir":
            if os.path.isdir(file_path):
                if self.accession_prefix:
                    accession_ref = self.accession_prefix + delimiter + str(self.accession_count)
                else:
                    accession_ref = self.accession_count
                self.accession_count += 1
            else:
                if self.accession_prefix:
                    accession_ref = self.accession_prefix + delimiter + "File"
                else:
                    accession_ref = "File"
        elif self.accession_flag.lower() == "all":
            if self.accession_prefix:
                accession_ref = self.accession_prefix + delimiter + str(self.accession_count)
            else:
                if self.accession_prefix:
                    accession_ref = self.accession_prefix + self.accession_count
                else:
                    accession_ref = self.accession_count
                self.accession_count += 1
        return accession_ref

    def main(self):
        """
        Runs Program :)
        """
        if self.empty_flag:
            self.remove_empty_directories()
        self.init_dataframe()
        output_file = define_output_file(self.output_path, self.root, meta_dir_flag = self.meta_dir_flag, 
                                         output_format = self.output_format)
        if self.output_format == "xlsx":
            export_xl(df = self.df, output_filename = output_file)
        elif self.output_format == "csv":
            export_csv(df = self.df, output_filename = output_file)
        elif self.output_format == "ods":
            export_ods(df = self.df, output_filename = output_file)
        elif self.output_format == "json":
            export_json(df = self.df, output_filename = output_file)
        elif self.output_format == "xml":
            export_xml(df = self.df, output_filename = output_file)
        elif self.output_format == "dict":
            return export_dict(df = self.df)

        print_running_time(self.start_time)
