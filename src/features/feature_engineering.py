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

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.preprocessing import MinMaxScaler

class Feature_Engineering(object):
    """ 
    Class with preprocessments to apply in dataframe
    """
    def __init__(self):
        super().__init__()
    
    def identify_num_values(self):
        """
        Set values that not correspond to a valid as np.NAN
        """


    def encode_anomalie(self,df,anomalies_column,amolalie_code = 'Q909'):
        #Q909 - Sindrome de Down
        df_copy = df.copy()
        df_copy[anomalies_column] = df_copy[anomalies_column].fillna('')
        df_copy[amolalie_code] = df_copy[anomalies_column].str.contains(amolalie_code).astype(int)
        return df_copy

    def balance_dataset(self,df):
        raise NotImplementedError()
        return df

    def convert_tabulars_to_timeseries(self):
        raise NotImplementedError()
        return df

    def define_categorical_and_continuous_columns(self,df,column_type_dict):
        raise NotImplementedError()
        return df

    def convert_missing_values_to_nan(self,df,columns_nan_value_dict):
        accepted_as_nan_values = [None]
        df.isnull().any(axis=1)
        return df

    def one_hot_encode_columns(self,df,column):
        df_copy = df.copy()
        df_copy = pd.get_dummies(df_copy[column])
        df_copy = df_copy.drop(column,axis = 1)
        # Join the encoded df
        df_copy = df_copy.join(one_hot_type)
        return df_copy

    def fit_normalizer(df_train,normalization_strategy):
        if 'min_max_scaler':
            scaler = MinMaxScaler()
            scaler.fit(df_train)
        return scaler

    def normalize_data(self,df,scaler):
        df_norm = scaler.transform(df)
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