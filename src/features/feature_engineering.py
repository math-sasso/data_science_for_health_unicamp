"""
Feature Engineering Steps

1.Imputation
2.Handling Outliers
3.Binning
4.Log Transform
5.One-Hot Encoding
6.Grouping Operations
7.Feature Split
8.Scaling
9.Extracting Date
https://towardsdatascience.com/feature-engineering-for-machine-learning-3a5e293a5114
"""

##TODO: Fazer a classe preprocessing conter instancias de pequenas partes da etapa de pre processamento. Inputer, Feature Engineering, etc...
import os
import sys
import pandas as pd
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.base import TransformerMixin
from typing import List
from ..io_utils import IO_Utils


class Feature_Engineering(object):
    """ 
    Class with preprocessments to apply in dataframe
    """
    def __init__(self):
        super().__init__()
        self.io_utils = IO_Utils()
        self.wordk_dir = os.path.dirname(__file__)
        self.data_dir = os.path.join(self.wordk_dir,'..','..','data')
        self.categorical_maps = self.io_utils.read_categorical_maps(json_file_path=os.path.join(self.data_dir,'interim','categorical_maps.json'))
    
    def fill_categorical_no_present_classes(self,df_cats):
        for columns,possible_values in self.categorical_maps.items():
            for _,value in possible_values.items():
                #import pdb;pdb.set_trace()
                if value not in df_cats.columns:
                    df_cats[value] = [0]*len(df_cats)
        
        return df_cats


    def iterative_inputer_integer(self,df):
        df_copy = df.copy()
        imp = IterativeImputer(max_iter=10, random_state=0)
        imp.fit(df_copy)
        df_new = pd.DataFrame(np.round(imp.transform(df_copy)), columns = df_copy.columns)
        df_new = df_new.astype('int32')
        return df_new
    
    def max_freq_inputer(self,df):
        df_copy = df.copy()
        imp = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
        df_new = pd.DataFrame(imp.fit_transform(df_copy),columns=df_copy.columns,index=df_copy.index)
        df_new = df_new.astype('category')
        #df_new[df_new.columns] = df_new[df_new.columns].astype('category')
        return df_new

    def get_cat_columns_in_codes(self,df_cat):
        df_cat_copy = df_cat.copy()
        for column in df_cat_copy.columns:
            df_cat_copy[column] = df_cat_copy[column].cat.codes
            df_cat_copy[column].replace({-1:np.nan},inplace=True)
        return df_cat_copy

    def _split_df_in_xy(self,df,target_column):
        df_copy = df.copy()
        X = df_copy.drop(target_column,axis = 1)
        y = df_copy[target_column]
        return X,y

    def encode_anomalie(self,df,anomalies_column,anomalie_code = 'Q909'):
        #Q909 Q900 - Sindrome de Down
        df_copy = df.copy()
        df_copy[anomalies_column] = df_copy[anomalies_column].fillna('')
        df_copy[anomalie_code] = df_copy[anomalies_column].str.contains(anomalie_code).astype(int)
        return df_copy

    def balance_dataset(self,df):
        raise NotImplementedError()
        return df

    def convert_tabulars_to_timeseries(self):
        # -> Colunas chave'DTNASC', 'HORANASC' ,'DTCADASTRO' , 'DIFDATA
        raise NotImplementedError()
        return df

    def define_categorical_and_continuous_columns(self,df,column_type_dict):
        raise NotImplementedError()
        return df

    def convert_missing_values_to_nan(self,df,columns_nan_value_dict):
        accepted_as_nan_values = [None]
        df.isnull().any(axis=1)
        return df

    def one_hot_encode_columns(self,df,columns):
        df_copy = df.copy()
        for column in columns:
            one_hot_encoded_column = pd.get_dummies(df_copy[column])
            df_copy = df_copy.drop(column,axis = 1)
            # Join the encoded df
            df_copy = df_copy.join(one_hot_encoded_column)
        return df_copy

    def fit_normalizer(self,df_train,normalization_strategy):
        if 'min_max_scaler':
            scaler = MinMaxScaler()
            scaler.fit(df_train)
        return scaler

    def normalize_data(self,df,scaler):
        cols = df.columns
        norm_data = scaler.transform(df)
        df_norm = pd.DataFrame(norm_data,columns=cols)
        return df_norm

    def convert_column_to_categorical(self,df,column):
        df[f'{column}_cat'] = df[column] 
        dict_maps = {category:i for i,category in enumerate(df[column].unique())}
        replace_rule = {f'{column}_cat':dict_maps}
        df = df.replace(replace_rule)

        return dict_maps,df

    def treat_df_missing_values(self,df,strategy):
        """
        Treat missing values according to a passed strategy
        """
        strategies = ['fill_with_predictons','eliminate_row','fill_mean','fill_last','fill_next','fill_aleatory']
        if strategy not in strategies:
            raise ValueError(f"O argumento strategy deve estar entre as estratégias {strategies}")
        
        if strategy == 'fill_with_predictons':
            pass
        
        
        threshold = 0.7

        #Dropping columns with missing value rate higher than threshold
        data = data[data.columns[data.isnull().mean() < threshold]]

        #Dropping rows with missing value rate higher than threshold
        data = data.loc[data.isnull().mean(axis=1) < threshold]

        raise NotImplementedError()
        return df