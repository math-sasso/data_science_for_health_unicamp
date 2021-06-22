import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
import pickle
root_dir = os.path.join(os.path.abspath(os.getcwd()).replace('= ',''))
sys.path.append(root_dir)
from src.features.feature_selection import Feature_Selection
from src.features.feature_engineering import Feature_Engineering
from src.data.retrievers import SINASC_Retriever

data_dir = os.path.join(root_dir,'data')
processed_data_dir = os.path.join(data_dir,'processed')
small_data_dir = os.path.join(root_dir,'small_data')


dict_cat = {'CONSULTAS':{2:'1 a 3 consultas',3:'4 a 6 consultas',4:'7 ou mais consultas'},
'ESCMAE':{1:'Sem escolaridade',2:'1ª a 3ª série',3:'4ª a 7ª série',4:'8ª a 3º colegial série',5:'Graduação'},
'ESTCIVMAE':{1:'Solteira',2:'Casada',3:'Viuvo',4:'Separado Judicial',5:'Unio Estavel'},
'GESTACAO':{1:'22 ou menos semanas de gestação',2:'22 a 27 semanas de gestação',3:'28 a 31 semanas de gestação',4:'32 a 36 semanas de gestação',5:'37 a 41 semanas de gestação',6:'22 ou mais semanas de gestação'},
'GRAVIDEZ':{1:'Gravidez única',2:'Gravidez dupla',3:'Gravidez tripla ou mais'},
'PARTO':{1:'Parto vaginal',2:'Parto cesareo'},
'RACACOR':{1:'Raça branca',2:'Raça preta',3:'Raça amarela',4:'Raça parda',5:'Raça indigena'},
'RACACORMAE':{1:'Raça mãe branca',2:'Raça mãe preta',3:'Raça mãe amarela',4:'Raça mãe parda',5:'Raça mãe indigena'},
'SEXO':{0:'Sexo inconclusivo',1:'Sexo Masculino',2:'Sexo Feminino'},
'STCESPARTO':{1:'Sim',2:'Não',3:'Não se aplica'},
'STTRABPART':{1:'Sim',2:'Não',3:'Não se aplica'},
'TPAPRESENT':{1:'Cefálico',2:'Pelvica ou Podálica',3:'Transversa'},
'TPROBSON':{1:'Robson 1',2:'Robson 2',3:'Robson 3',4:'Robson 4',5:'Robson 5',6:'Robson 6',7:'Robson 7',8:'Robson 8',9:'Robson 9',10:'Robson 10',11:'Robson 11'},
}

dict_cat_orig = {
'CONSULTAS':{2:'1_3_consultas',3:'4_6_consultas',4:'7_+_consultas'},
'ESCMAE':{1:'sem_esc',2:'1_3_esc',3:'4_7_esc',4:'8_11_esc',5:'12_+_esc'},
'ESTCIVMAE':{1:'Solteiro',2:'Casado',3:'Viuvo',4:'Separado_Judicial',5:'Uniao_Estavel'},
'GESTACAO':{1:'22_-_semgest',2:'22_27_semgest',3:'28_31_semgest',4:'32_36_semgest',5:'37_41_semgest',6:'42_+_semgest'},
'GRAVIDEZ':{1:'grav_unica',2:'grav_dupla',3:'grav_tripla+'},
'PARTO':{1:'parto_vaginal',2:'parto_cesareo'},
'RACACOR':{1:'raca_branca',2:'raca_preta',3:'raca_amarela',4:'raca_parda',5:'raca_indigena'},
'RACACORMAE':{1:'raca_mae_branca',2:'raca_mae_preta',3:'raca_mae_amarela',4:'raca_mae_parda',5:'raca_mae_indigena'},
'SEXO':{0:'sexo_inc',1:'sexo_mas',2:'sexo_fem'},
'STCESPARTO':{1:'stcesparto_ces_antes',2:'stcesparto_ces_apos',3:'stcesparto_naplica'},
'STTRABPART':{1:'sttrabpart_sim',2:'sttrabpart_nao',3:'sttrabpart_naplica'},
'TPAPRESENT':{1:'tpa_cefalico',2:'tpa_pelvica_oupudalica',3:'tpa_transversa'},
'TPROBSON':{1:'robson_1',2:'robson_2',3:'robson_3',4:'robson_4',5:'robson_5',6:'robson_6',7:'robson_7',8:'robson_8',9:'robson_9',10:'robson_10',11:'robson_11'},
}

dict_model = {}
for (k1,v1),(k2,v2) in zip(dict_cat.items(),dict_cat_orig.items()):
    dict_model[k1] = {v_1:v_2 for (k_1,v_1),(k_2,v_2) in zip(v1.items(),v2.items())}

retriever = SINASC_Retriever()
fe = Feature_Engineering()
fs = Feature_Selection()
 

st.write("""
# Preditor de Sindrome de Down com dados do SINASC
O objetivo desta aplicação é predizer a partir das variáveis de entrada disponibilizadas pelo DATASUS se um recém nascido possui ou não síndrome de down.
Dados obtidos do SINASC [palmerpenguins library](http://tabnet.datasus.gov.br/cgi/deftohtm.exe?SINASC/anomalias/anomabr.def), plataforma de daddos de recém nascidos do DATASUS
""")

st.sidebar.header('Variáveis de entrada')

st.sidebar.markdown("""
[Exemplo de CSV de entrada](https://raw.githubusercontent.com/dataprofessor/data/master/penguins_example.csv)
""")

# Collects user input features into dataframe
uploaded_file = st.sidebar.file_uploader("Insira o seu CSV aquis", type=["csv"])
if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
else:
    #streamlit.slider(label, min_value=None, max_value=None, value=None, step=None, format=None, key=None, help=None)
    def user_input_features():
        ESTCIVMAE = st.sidebar.selectbox("Situação conjugal da mãe",tuple(dict_cat['ESTCIVMAE'].values()))
        ESCMAE = st.sidebar.selectbox("Escolaridade da mãe",tuple(dict_cat['ESCMAE'].values()))
        GESTACAO =  st.sidebar.selectbox("Classificação semanas de gestação",tuple(dict_cat['GESTACAO'].values()))
        GRAVIDEZ =  st.sidebar.selectbox("Tipo de gravidez",tuple(dict_cat['GRAVIDEZ'].values()))
        PARTO = st.sidebar.selectbox("Tipo de parto",tuple(dict_cat['PARTO'].values()))
        CONSULTAS =  st.sidebar.selectbox("Quantidade de consultas",tuple(dict_cat['CONSULTAS'].values()))
        SEXO = st.sidebar.selectbox("Sexo",tuple(dict_cat['SEXO'].values()))
        RACACOR = st.sidebar.selectbox("Raça",tuple(dict_cat['RACACOR'].values()))
        RACACORMAE = st.sidebar.selectbox("Raça da mãe",tuple(dict_cat['RACACORMAE'].values()))
        TPAPRESENT = st.sidebar.selectbox("Tipo de apresentação do recém nascido",tuple(dict_cat['TPAPRESENT'].values()))
        STTRABPART = st.sidebar.selectbox("Trabalho de parto induzido?",tuple(dict_cat['STTRABPART'].values()))
        STCESPARTO = st.sidebar.selectbox("Cesárea ocorreu antes do trabalho de parto iniciar?",tuple(dict_cat['STCESPARTO'].values()))
        TPROBSON = st.sidebar.selectbox("Indíce trobson",tuple(dict_cat['TPROBSON'].values()))
        IDADEMAE=st.sidebar.slider('Idade da mãe', 13,45,25,step=1)
        QTDFILVIVO = st.sidebar.slider("Quantidade de filhos vivos",0,9,1,step=1) 
        QTDFILMORT = st.sidebar.slider("Quantidade de perdas fetais ou abortos",0,6,0,step=1) 
        APGAR1 = st.sidebar.slider('APGAR1', 0,10,10,step=1)
        APGAR5 = st.sidebar.slider('APGAR5', 0,10,10,step=1)
        PESO = st.sidebar.slider('Peso ao nascer em gramas', 1,9000,3000,step=1)
        QTDGESTANT = st.sidebar.slider("Quantidade de gestações anteriores",0,30,1,step=1) 
        QTDPARTNOR = st.sidebar.slider("Quantidade de partos normais anteriores",0,30,1,step=1)
        QTDPARTCES = st.sidebar.slider("Quantidade de partos cesariana anteriores",0,30,1,step=1 )
        IDADEPAI = st.sidebar.slider("Idade do pai",10,65,30,step=1) 
        SEMAGESTAC = st.sidebar.slider("Número de semanas de gestação",1,50,40,step=1) 
        CONSPRENAT = st.sidebar.slider("Número de cosultas pré natal",1,50,40,step=1) 
        MESPRENAT = st.sidebar.slider("Mês de gestação em que iniciou o pré‐natal",1,9,5,step=1)

        data = {
        'ESTCIVMAE': dict_model['ESTCIVMAE'][ESTCIVMAE],
        'ESCMAE':dict_model['ESCMAE'][ESCMAE] ,
        'GESTACAO':dict_model['GESTACAO'][GESTACAO] ,
        'GRAVIDEZ':dict_model['GRAVIDEZ'][GRAVIDEZ] ,
        'PARTO':dict_model['PARTO'][PARTO] ,
        'CONSULTAS':dict_model['CONSULTAS'][CONSULTAS] ,
        'SEXO':dict_model['SEXO'][SEXO] ,
        'RACACOR':dict_model['RACACOR'][RACACOR] ,
        'RACACORMAE':dict_model['RACACORMAE'][RACACORMAE] ,
        'TPAPRESENT':dict_model['TPAPRESENT'][TPAPRESENT] ,
        'STTRABPART':dict_model['STTRABPART'][STTRABPART] ,
        'STCESPARTO':dict_model['STCESPARTO'][STCESPARTO] ,
        'TPROBSON':dict_model['TPROBSON'][TPROBSON] ,
        'IDADEMAE': IDADEMAE,
        'QTDFILVIVO':QTDFILVIVO ,
        'QTDFILMORT':QTDFILMORT ,
        'APGAR1':APGAR1 ,
        'APGAR5':APGAR5 ,
        'PESO':PESO ,
        'QTDGESTANT':QTDGESTANT ,
        'QTDPARTNOR':QTDPARTNOR ,
        'QTDPARTCES':QTDPARTCES ,
        'IDADEPAI':IDADEPAI ,
        'SEMAGESTAC':SEMAGESTAC ,
        'CONSPRENAT':CONSPRENAT ,
        'MESPRENAT':MESPRENAT}

        features = pd.DataFrame(data, index=[0])
        return features
    input_df = user_input_features()

# Combines user input features with entire penguins dataset
# This will be useful for the encoding phase
#data_raw = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv')
#penguins = data_raw.drop(columns=['species'], axis=1)
#df = pd.concat([input_df,penguins],axis=0)
df = input_df
# Encoding of ordinal features
# https://www.kaggle.com/pratik1120/penguin-dataset-eda-classification-and-clustering
df = retriever.map_columns_as_categoricals(df)
df_cats = df.select_dtypes(['category'])
df_consts = df[[x for x in df.columns if x not in df_cats.columns]] 
#df_cats_imp = fe.max_freq_inputer(df_cats)
#df_consts_imp = fe.iterative_inputer_integer(df_consts)
df_cats_codes = fe.get_cat_columns_in_codes(df_cats)
df_cats = fe.one_hot_encode_columns(df_cats,df_cats.columns)
for k,v in dict_cat_orig.items():
    for _,v_ in v.items():
        #import pdb;pdb.set_trace()
        if v_ not in df_cats.columns:
            df_cats[v_] = [0]

#import pdb;pdb.set_trace()
df = df_cats.join(df_consts)
df = df[:1] # Selects only the first row (the user input data)

# Displays the user input features
st.subheader('Entradas do usuário')

if uploaded_file is not None:
    st.write(df)
else:
    st.write('Esperando por CSV a ser carregado')
    st.write(df)

# Reads in saved classification model
filepath = os.path.join(small_data_dir,'rf_model_sdown.sav')
load_clf = pickle.load(open(filepath, 'rb'))

# Apply model to make predictions
prediction = load_clf.predict(df)
prediction_proba = load_clf.predict_proba(df)

st.subheader('Predição')
options = np.array(['Sindrome de Down presente','Sindrome de Down ausente'])
st.write(options[prediction])