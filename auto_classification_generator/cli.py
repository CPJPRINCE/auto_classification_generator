from auto_classification_generator.classification_generator import ClassificationGenerator
import argparse, os
import importlib.metadata

def parse_args():
    parser = argparse.ArgumentParser(description = "Auto Classification Generator for Digital Cataloguing")
    parser.add_argument('root', nargs = '?', default = os.getcwd(),
                        help = "The root directory to create references for")
    parser.add_argument("-p", "--prefix", required = False, nargs = '?',
                        help = "Set a prefix to append onto generated references")
    parser.add_argument("--rm-empty", required = False, action = 'store_true',
                        help = "Sets the Program to remove any Empty Directory and Log removals to a text file")
    parser.add_argument("-acc", "--accession", required = False, choices = ['none', 'dir', 'file', 'all'], default = None, type = str.lower,
                        help="Sets the program to create an accession listing - IE a running number of the files.")
    parser.add_argument("-accp", "--acc-prefix", required = False, nargs = '?',
                        help = "Sets the Prefix for Accession Mode")
    parser.add_argument("-o", "--output", required = False, nargs = '?',
                        help = "Set the output directory for created spreadsheet")
    parser.add_argument("-s", "--start-ref", required = False, nargs = '?', default = 1,
                        help = "Set the starting reference number. Won't affect sub-folders/files")
    parser.add_argument("-dlm", "--delimiter", required = False, nargs= '?',type = str,
                        help = "Set the delimiter to use between levels")
    parser.add_argument("--disable-meta-dir", required = False, action = 'store_true', default = True,
                        help = "Set to disable creating a 'meta' file for spreadsheet; can be used in combination with output")
    parser.add_argument("--skip", required = False, action = 'store_true', default = False,
                        help = "Set to skip creating references, will generate a spreadsheet listing")
    parser.add_argument("--hidden", required = False , action = 'store_true', default = False,
                        help = "Set to include hidden files/folders in the listing")
    parser.add_argument("-fmt", "--output-format", required = False, default = "xlsx", choices = ['xlsx', 'csv', 'json', 'ods', 'xml', 'dict'],
                        help = "Set to set output format. Note ods requires odfpy; xml requires lxml")
    parser.add_argument("-fx", "--fixity", required = False, nargs = '?', const = "SHA-1", default = None, choices = ['NONE', 'MD5', 'SHA-1', 'SHA-256', 'SHA-512'], type = str.upper,
                        help = "Set to generate fixtites, specify Algorithm to use")
    parser.add_argument("-v", "--version", action = 'version', version = '%(prog)s {version}'.format(version = importlib.metadata.version("auto_classification_generator")),
                        help = "See version information")
    parser.add_argument("-key","--keywords", nargs = '*', default = None,
                        help = "Set to replace reference numbers with given Keywords - Must be exact matches, case sensistive")
    parser.add_argument("-keym","--keywords-mode", nargs = '?', const = "intialise", choices = ['intialise','firstletters'], default = 'intialise',
                        help = "Set to alternate keyword mode: 'intialise' will use intials of words; 'firstletters' will use the first letters of the string")
    parser.add_argument("--keywords-retain-order", required = False, default = False, action = 'store_true', 
                        help = "Set when using keywords to continue reference numbering. If not used keywords don't 'count' to reference numbering")
    parser.add_argument("--keywords-abbreviation-number", required = False, nargs='+', default = None, type = int,
                        help = "Set to set the number of letters to abbreviate for 'firstletters' mode, does not impact 'intialise' [currently]")
    parser.add_argument("--sort-by", required=False, nargs = '?', default = 'foldersfirst', choices = ['foldersfirst','alphabetical'], type=str.lower,
                        help = "Set the sorting method, 'foldersfirst' sorts folders first then files alphabetically; 'alphabetically' sorts alphabetically (ignoring folder distinction)")
    args = parser.parse_args()
    return args

def run_cli():
    args = parse_args()
    if isinstance(args.root, str):
        args.root = args.root.strip("\"").rstrip("\\")
    if not args.output:
        args.output = os.path.abspath(args.root)
        print(f'Output path defaulting to root directory: {args.output}')
    else:
        args.output = os.path.abspath(args.output)
        print(f'Output path set to: {args.output}')
    if args.sort_by:
        if args.sort_by == "foldersfirst":
            sort_key = lambda x: (os.path.isfile(x), str.casefold(x))
        elif args.sort_by == "alphabetical":
            sort_key = str.casefold

    ClassificationGenerator(args.root, 
                            output_path = args.output, 
                            prefix = args.prefix, 
                            accprefix = args.acc_prefix, 
                            fixity = args.fixity, 
                            empty_flag = args.rm_empty, 
                            accession_flag = args.accession, 
                            hidden_flag = args.hidden, 
                            start_ref = args.start_ref, 
                            meta_dir_flag = args.disable_meta_dir, 
                            skip_flag = args.skip, 
                            output_format = args.output_format,
                            keywords = args.keywords,
                            keywords_mode = args.keywords_mode,
                            keywords_retain_order = args.keywords_retain_order,
                            sort_key = sort_key,
                            delimiter = args.delimiter,
                            keywords_abbreviation_number = args.keywords_abbreviation_number).main()
    print('Complete!')

if __name__ == "__main__":
    run_cli()