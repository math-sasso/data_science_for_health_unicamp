import os
import json
import pandas as pd
from pickle import load as load_pickle
from pickle import dump as dump_pickle


class IO_Utils(object):
    """ 
    Class with utilities for reading and writing
    """
    def __init__(self):
        pass


    def load_pickle(self,filepath):
        with open(filepath, 'rb') as f:
            content = load_pickle(f)
        return content

    def save_pickle(self,filepath,info):
        """
        Save info in a picke file
        """
        with open(filepath, 'wb') as f:
            dump_pickle(info, f)

    def read_json(self,json_file_path):
        with open(json_file_path) as f:
            json_result = json.load(f)
        return json_result

    def read_categorical_maps(self,json_file_path):
        with open(json_file_path) as f:
            json_result = json.load(f)
        json_result = {outer_k:{int(k):v for k,v in outer_v.items() } for outer_k,outer_v in json_result.items()}
        return json_result
        
    
    def create_folder_structure(self,folder):
        """ Create the comple folder structure if it does not exists """
        if not os.path.exists(folder):
            os.makedirs(folder)
            
    def save_json(self,destination_path,d,ensure_ascii=False,command='a'):
        with open(destination_path, command) as fp:
            json.dump(d, fp, ensure_ascii=ensure_ascii)

    def read_txt_file(self,txt_file_path):
        with open(txt_file_path) as f:
            txt_result = f.read().split("\n")
        return txt_result

    def save_df_zipped_csv(self,df,dirpath,file_name):

        #compression_opts = dict( ompression='gzip', archive_name=os.path.join(dirpath,f'{file_name}.csv'))  
        df.to_csv(os.path.join(dirpath,f'{file_name}.csv.gz'), index=False, compression='gzip')

    def read_zipped_csv_df(self,dirpath,file_name):
        #zf = zipfile.ZipFile(os.path.join(dirpath,f'{file_name}.csv.gz'))
        df = pd.read_csv(os.path.join(dirpath,f'{file_name}.csv.gz'))
        return df

    def read_cnv_file_as_df(self,cnv_file_path,columns=None,special_pasing_method=None):
        with open(cnv_file_path,errors="ignore") as f:
            txt_result = f.read().split("\n")
            if special_pasing_method:
                list_df_rows = special_pasing_method(txt_result)
            else:
                list_df_rows =[list(filter(None, row.split('  '))) for row in txt_result]
            list_df_rows = list_df_rows[1:-1]
            list_df_rows = [x for x in list_df_rows if x]
            list_df_rows = [[elem.strip() for elem in row] for row in list_df_rows]
            _ = [l.pop(0) for l in list_df_rows]
            # if any(len(list_df_rows[0])!= len(i) for i in list_df_rows):
            df = pd.DataFrame(list_df_rows,columns=None)
        return df