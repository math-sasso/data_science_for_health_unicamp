import os
import sys
# import pdb;pdb.set_trace()
sys.path.append(os.path.abspath(os.getcwd()))
import pandas as pd
import pdb
import seaborn as sns
import matplotlib.pyplot as plt
#from sklearn.model_selection import train_test_split
from src.features.feature_selection import Feature_Selection
from src.features.feature_engineering import Feature_Engineering
from src.data.retrievers import SINASC_Retriever
from src.io_utils import IO_Utils

#Variáveis de Interesse
target_anomalies = ['Q900','Q901','Q902','Q903','Q904','Q905','Q906','Q907','Q908','Q909']
target_years = list(range(2010,2020))
target_states = ['SP']

#Setting Paths
data_dir = os.path.join(os.path.dirname(__file__),'..','data')
processed_data_dir = os.path.join(data_dir,'processed')
#sp_2019_path  = os.path.join(data_dir,'external','SINASC_DATA','SP','SP_2019.zip')

# Creating helping classes instances
retriever = SINASC_Retriever()
fe = Feature_Engineering()
fs = Feature_Selection()
io_utils = IO_Utils()

# Creating Dadasets (only once)
# df_anomalies = retriever.extract_rows_anomalie(states=target_states,
#                                                 years=target_years,
#                                                 anomalie_codes=target_anomalies,
#                                                 anomalies_present=True)
# io_utils.save_df_zipped_csv(df=df_anomalies,dirpath=processed_data_dir,file_name='df_sindrome_down')
# df_no_anomalies = retriever.extract_rows_anomalie(states=target_states,
#                                                 years=target_years,
#                                                 anomalie_codes=target_anomalies,
#                                                 anomalies_present=False)

# io_utils.save_df_zipped_csv(df=df_no_anomalies,dirpath=processed_data_dir,file_name='df_no_sindrome_down')
# df_no_anomalies_cropped = df_no_anomalies.sample(frac=1)[:len(df_anomalies)]
# io_utils.save_df_zipped_csv(df=df_no_anomalies,dirpath=processed_data_dir,file_name='df_no_anomalies_cropped')

# Retrieving Datasets
import pdb;pdb.set_trace()
df_anomalies = pd.read_csv(os.path.join(processed_data_dir,'df_anomalies.zip'))
df_no_anomalies_cropped = pd.read_csv(os.path.join(processed_data_dir,'df_no_anomalies_cropped.zip'))


os.path.join(data_dir,'external','SINASC_DATA','SP')
# Performing Feature Selection


import pdb;pdb.set_trace()
df = fe.special_read_csv(path = sp_2019_path)
df_econded = fe.encode_anomalie(df,'CODANOMAL',amolalie_code = target_anomal)
X,y = fe._split_df_in_xy(df_econded,target_column='CODANOMAL')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = fe.fit_normalizer(df_train=X_train ,normalization_strategy='min_max_scaler')
X_train = fe.normalize_data(X_train,scaler)
X_test = fe.normalize_data(X_test,scaler)
import pdb;pdb.set_trace()
#target_correlation = fs.get_correlation_with_target(df_econded,'Q909','pearson')
chi_square = fs.get_chisquare_feature_scores(df_econded,target_column=target_anomal,n_features_to_select=10)
import pdb;pdb.set_trace()
chi_square
# fig = plt.figure(figsize=(36,36))
# heatmap = sns.heatmap(df.corr(), vmin=-1, vmax=1, annot=True, cmap='coolwarm',fmt = '.2f')
# heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':18}, pad=12)
# plt.show()
