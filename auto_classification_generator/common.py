"""
Common Tools used in both Opex Manifest and Auto CLassificaiton modules. Exporting to Excel, CSV.

author: Christopher Prince
license: Apache License 2.0"
"""

import os
import time
import pandas as pd
import sys

def path_check(path):
    if os.path.exists(path):
        pass
    else: os.makedirs(path)

def define_output_file(output_path,output_name,meta_dir_flag=True,output_suffix="_AutoClass",output_format="xlsx"):
    path_check(output_path)
    if meta_dir_flag:
        path_check(os.path.join(output_path,"meta"))
        output_dir = os.path.join(output_path,"meta",str(os.path.basename(output_name)) + output_suffix + "." + output_format)
    else: output_dir = os.path.join(output_path,str(os.path.basename(output_name)) + output_suffix + "." + output_format)
    return output_dir

def export_list_txt(txt_list,output_filename):
    try: 
        with open(output_filename,'w') as writer:
            for line in txt_list:
                writer.write(f"{line}\n")
    except Exception as e:
        print(e)
        print('Waiting 10 Seconds to try again...')
        time.sleep(10)
        export_list_txt(txt_list,output_filename)
    finally:
        print(f"Saved to: {output_filename}")

def export_csv(df,output_filename):
    try:
        df['Archive_Reference'] = df['Archive_Reference'].astype('string')
        df.to_csv(output_filename,sep=",",encoding="utf-8")
    except Exception as e:
        print(e)
        print('Waiting 10 Seconds to try again...')
        time.sleep(10)
        export_csv(df,output_filename)
    finally:
        print(f"Saved to: {output_filename}")

def export_xl(df,output_filename):
    try:
        with pd.ExcelWriter(output_filename,mode='w') as writer:
            df.to_excel(writer)
    except Exception as e:
        print(e)
        print('Waiting 10 Seconds to try again...')
        time.sleep(10)
        export_xl(df,output_filename)
    finally:
        print(f"Saved to: {output_filename}")

def win_256_check(path: str):
    if len(path) > 255 and sys.platform == "win32":
        if path.startswith(u'\\\\?\\'): path = path
        else: path = u"\\\\?\\" + path
    return path