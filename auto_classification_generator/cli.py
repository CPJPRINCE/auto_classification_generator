from auto_classification_generator.classification_generator import ClassificationGenerator
import argparse
import os
import importlib.metadata

def parse_args():
    parser = argparse.ArgumentParser(description="OPEX Manifest Generator for Preservica Uploads")
    parser.add_argument('root',nargs='?', default=os.getcwd())
    parser.add_argument("-p","--prefix",required=False, nargs='?')
    parser.add_argument("-accp", "--acc-prefix",required=False, nargs='?')
    parser.add_argument("-rm","--empty",required=False,action='store_true')
    parser.add_argument("-acc","--accession",required=False,choices=['None','Dir','File','All'],default=None)
    parser.add_argument("-o","--output",required=False,nargs='?')
    parser.add_argument("-s","--start-ref",required=False,nargs='?',default=1)
    parser.add_argument("--meta-dir",required=False,action='store_true',default=True)
    parser.add_argument("--skip",required=False,action='store_true',default=False)
    parser.add_argument("--hidden",required=False,action='store_true',default=False)
    parser.add_argument("-fmt","--output-format",required=False,default="xlsx",choices=['xlsx','csv'])
    parser.add_argument("-fx","--fixity",required=False,nargs='?', const="SHA-1",default=None,choices=['NONE','MD5','SHA-1','SHA-256','SHA-512'],type=str.upper)
    parser.add_argument("-v", "--version", action='version',version='%(prog)s {version}'.format(version=importlib.metadata.version("auto_classification_generator")))
    args = parser.parse_args()
    return args

def run_cli():
    args = parse_args()
    if isinstance(args.root,str): args.root = args.root.strip("\"").rstrip("\\")
    if not args.output:
        args.output = os.path.abspath(args.root)
        print(f'Output path defaulting to root directory: {args.output}')
    else:
        args.output = os.path.abspath(args.output)
        print(f'Output path set to: {args.output}')
    
    ClassificationGenerator(args.root,
                            output_path = args.output,
                            prefix=args.prefix,
                            accprefix=args.acc_prefix,
                            fixity=args.fixity,
                            empty_flag=args.empty,
                            accession_flag=args.accession,
                            hidden_flag=args.hidden,
                            start_ref=args.start_ref,
                            meta_dir_flag=args.meta_dir,
                            skip_flag=args.skip,
                            output_format=args.output_format).main()
    print('Complete!')