import os
import pandas as pd
import pdb
import seaborn as sns
import matplotlib.pyplot as plt
from feature_selection import Feature_Selection
from feature_engineering import Feature_Engineering

target_anomal = 'Q909'
root_dir = os.path.join(os.path.abspath(os.getcwd()).replace('= ',''))
data_dir = os.path.join(root_dir,'data')
df = pd.read_csv(os.path.join(data_dir,'external','SINASC_DATA','SP','SP_2009.zip'))
fe = Feature_Engineering()
df_econded = fe.encode_anomalie(df,'CODANOMAL',amolalie_code = target_anomal)
fs = Feature_Selection()
#target_correlation = fs.get_correlation_with_target(df_econded,'Q909','pearson')
chi_square = fs.get_chisquare_feature_scores(df_econded,target_column=target_anomal,n_features_to_select=10)
import pdb;pdb.set_trace()
chi_square
# fig = plt.figure(figsize=(36,36))
# heatmap = sns.heatmap(df.corr(), vmin=-1, vmax=1, annot=True, cmap='coolwarm',fmt = '.2f')
# heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':18}, pad=12)
# plt.show()