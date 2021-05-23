import os
import numpy as np
import pandas as pd
from typing import List
from pysus.online_data.sinasc import download
from ..io_utils import IO_Utils

class Retriever(object):
    def __init__(self):
        self.states_brasil = {
            'AC': 'Acre',
            'AL': 'Alagoas',
            'AP': 'Amapá',
            'AM': 'Amazonas',
            'BA': 'Bahia',
            'CE': 'Ceará',
            'DF': 'Distrito Federal',
            'ES': 'Espírito Santo',
            'GO': 'Goiás',
            'MA': 'Maranhão',
            'MT': 'Mato Grosso',
            'MS': 'Mato Grosso do Sul',
            'MG': 'Minas Gerais',
            'PA': 'Pará',
            'PB': 'Paraíba',
            'PR': 'Paraná',
            'PE': 'Pernambuco',
            'PI': 'Piauí',
            'RJ': 'Rio de Janeiro',
            'RN': 'Rio Grande do Norte',
            'RS': 'Rio Grande do Sul',
            'RO': 'Rondônia',
            'RR': 'Roraima',
            'SC': 'Santa Catarina',
            'SP': 'São Paulo',
            'SE': 'Sergipe',
            'TO': 'Tocantins'
        }
        self.wordk_dir = os.path.dirname(__file__)
        self.data_dir = os.path.join(self.wordk_dir,'..','..','data')
        self.io_utils = IO_Utils()
        self.acceptable_years = np.arange(2010,2020)
    
    def check_state_years_inputs_erros(self,states,years):
            if (type(years) != list) or not all(isinstance(i, int) for i in years):
                raise AttributeError("O argumento years deve ser uma lista de inteiros")
            
            if (type(years) != list) or not all(isinstance(i, str) for i in states):
                raise AttributeError("O argumento states deve ser uma lista de strings")

            if not set(years).issubset(self.acceptable_years):
                raise AttributeError("Todos os anos devem estar entre 1999 e 2019")
            
            if not set(states).issubset(self.states_brasil.keys()):
                raise AttributeError(f"Todos os estados devem estar na lista: {list(self.states_brasil.keys())}")


class SINASC_Retriever(Retriever):
    def __init__(self):
        super().__init__()
        self.sinasc_raw_dir = os.path.join(self.data_dir,'external','SINASC_DATA')

        self.columns_valid_values = {
            'APGAR1':[0,1,2,3,4,5,6,7,8,9,10],
            'APGAR5':[0,1,2,3,4,5,6,7,8,9,10],
            'CONSPRENAT':list(range(0, 51)),
            'CONSULTAS':[2,3,4],
            'ESCMAE':[1,2,3,4,5],
            # 'ESCMAE2010':[0,1,2,3,4,5],
            # 'ESCMAEAGR1':[2,3,4,5,6,7,8,9,10,11,12,13],
            'ESTCIVMAE':[1,3,4,5],
            'GESTACAO':[1,2,3,4,5,6],
            'GRAVIDEZ':[1,2,3],
            'IDADEMAE': list(range(10, 46)),
            'IDADEPAI':list(range(10, 66)),
            'MESPRENAT':[1,2,3,4,5,6,7,8,9],
            'PARTO':[1,2],
            'PESO':list(range(1, 9000)),
            'QTDFILMORT':list(range(0,10)),
            'QTDFILVIVO':list(range(0,10)),
            'QTDGESTANT':list(range(0,31)),
            'QTDPARTCES':list(range(0,31)),
            'QTDPARTNOR':list(range(0,31)),
            'RACACOR':[1,2,3,4,5],
            'RACACORMAE':[1,2,3,4,5],
            'SEMAGESTAC':list(range(1,51)),
            'SEXO':[0,1,2],
            'STCESPARTO':[1,2,3],
            'STTRABPART':[1,2,3],
            'TPAPRESENT':[1,2,3],
            # 'TPNASCASSI':[1,2,3,4],
            'TPROBSON':list(range(1,12))}

    def get_data(self,**kwargs):
       
        states = kwargs.get('states')
        years = kwargs.get('years')
        json_path = kwargs.get('json_path',None)
        
        #Removing Duplicates
        states = list(set(states))
        years = list(set(years))
        
        #Checking Errors
        self.check_state_years_inputs_erros(states,years)

        #Downloading Data
        json_result = self.io_utils.read_json(json_path) if json_path else {'metadata': {'column_descriptions':{}}}
        for state in states:
            for year in years:
                dir_path = os.path.join(self.sinasc_raw_dir,state)
                self.io_utils.create_folder_structure(folder=dir_path)
                if not os.path.exists(folder):
                    df = download(state, year)
                    year_str = str(year)
                    io_utils.save_df_zipped_csv(df=df,dirpath=dir_path,file_name=f'{state}_{year_str}')

    def extract_rows_anomalie(self,states:List[str],years:List[int],anomalie_codes:List[str],anomalies_present=True):
        
        #Removing Duplicates
        states = list(set(states))
        years = list(set(years))
        
        #Checking Errors
        self.check_state_years_inputs_erros(states,years)
        
        all_df_anomalies_list = []
        for state in states:
            state_dirpath = os.path.join(self.sinasc_raw_dir,state)
            for year in years:
                list_dfs_anomalies = []
                year = str(year)
                df = self.special_read_csv(os.path.join(state_dirpath,f'{state}_{year}.zip'))
                df['CODANOMAL'] = df['CODANOMAL'].fillna('')
                for anomalie_code in anomalie_codes:
                    if anomalies_present:
                        df_anomalie = df[df['CODANOMAL'].str.contains(anomalie_code)]
                    else:
                        df_anomalie = df[~df['CODANOMAL'].str.contains(anomalie_code)]
                    list_dfs_anomalies.append(df_anomalie)
                df_anomalies = pd.concat(list_dfs_anomalies, ignore_index=True).drop_duplicates()
                df_anomalies['STATE'] = state
                df_anomalies['YEAR'] = int(year)
 
                all_df_anomalies_list.append(df_anomalies)
        
        all_df = pd.concat(all_df_anomalies_list, ignore_index=True).drop_duplicates()
        if anomalies_present:
            all_df['ANOMAL_PRESENT'] = 1
        else:
            all_df['ANOMAL_PRESENT'] = 0
        return all_df

    def extract_rows_without_anomalie(self,states:List[str],years:List[str]):
        pass

    def _drop_trivials(self,df):
        #CODOCUPMAE - Pode ser uma variável interessante mas dificil de ser processada
        #NATURALMAE,CODPAISRES - Pais da mãe - pode ter alguma relação dependendo da anomalia
        #DTNASCMAE - Trivial com o IDADEMAE
        
        # df = df[df.columns.difference(['ORIGEM','CODESTAB','CODMUNNASC','CODMUNRES','IDANOMAL','DTNASC','HORANASC','DTCADASTRO','DIFDATA','CODMUNNATU','DTRECORIGA','CODUFNATU','NATURALMAE','DTNASCMAE','CODPAISRES','CODOCUPMAE','VERSAOSIST','NUMEROLOTE','DTDECLARAC', 'DTRECEBIM','SERIESCMAE','TPDOCRESP','TPFUNCRESP','TPMETESTIM'])]
        # df = df[df.columns.difference(['PARIDADE','KOTELCHUCK'])] #remoções temporárias por falta de explicalções das bases
        # df = df[df.columns.difference(['STDNEPIDEM', 'STDNNOVA'])] #provavelmente variaveis de controle da base
        # df = df[df.columns.difference(['DTULTMENST'])] #Dificil interpretação
        df.columns= df.columns.str.upper()
        all_columns = ['CODANOMAL','CONTADOR'] + list(self.columns_valid_values.keys())
        df.drop(df.columns.difference(all_columns), 1, inplace=True)
        # try:  
        #     df = df[all_columns]
        #     print(df.columns)
        # except:
        #     import pdb;pdb.set_trace()
        return df

    def special_read_csv(self,path):
        df = pd.read_csv(path)
        df = self._drop_trivials(df)
        # import pdb;pdb.set_trace()
        y = df['CODANOMAL']
        X =  df.drop('CODANOMAL',axis = 1)
        X = X.apply(pd.to_numeric,errors='coerce')
        for column in X:
            if column in list(self.columns_valid_values.keys()):
                X.loc[~X[column].isin(self.columns_valid_values[column]),column]=np.nan
        
        df = X.join(y)
        # self.print_unique_values(df)
        return df

    def print_unique_values(self,df):
        uniques_dict = {}
        for column in df.columns.difference(['CODANOMAL','CONTADOR']):
            uniques_dict[column] = list(df[column].unique())
        print(df)


    def map_columns_as_categoricals(self,df):
        df_copy = df.copy()
        categorical_maps = {
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
        
        for column in df_copy.columns:
            if column in list(categorical_maps.keys()):
                categories = categorical_maps[column]
                #df_copy[column] = df_copy[column].map(categories) 
                df_copy[column].replace(categories, inplace=True)
                #df['ESTCIVMAE'].astype('int32',errors='ignore')
                #df_copy[column].replace({-1:np.nan}, inplace=True)

        df_copy[list(categorical_maps.keys())] = df_copy[list(categorical_maps.keys())].astype('category')
        return df_copy














    # def _get_all_column_variables_descriptions(self):
    #     #codigos municipios
    #     #https://www.anatel.gov.br/dadosabertos/PDA/Codigo_Nacional/PGCN.csv
    #     #https://bigdata-metadados.icict.fiocruz.br/dataset/sistema-de-informacoes-de-nascidos-vivos-sinasc/resource/9d664e65-2dbd-44cf-8f4a-65499affa27c
    #     #http://www2.datasus.gov.br/DATASUS/index.php?area=0901&item=1&acao=28
    #     #http://svs.aids.gov.br/dantps/cgiae/sinasc/documentacao/
    #     tabdn_dir = os.path.join(self.data_dir,'raw','tabdn')
    #     jsons_tabdn_dir = os.path.join(self.data_dir,'raw','jsons_tabdn')
    #     columns_variables_descriptions = {'CODMUNNASC':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'MUNICBR.CNV'),columns=['codigo-cidade','codigos_aceitos','possivel_lixo']),\
    #     'LOCNASC':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'LOCOCOR.CNV')),\
    #     'IDADEMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'FXtabnet.cnv')),\
    #     'ESTCIVMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'ESTCIV.CNV')),\
    #     'ESCMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'INSTRUC.CNV')),\
    #     # 'CODOCUPMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'GRUPO1.CNV')),\
    #     # 'CODOCUPMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'GRUPO2.CNV')),\
    #     # 'CODOCUPMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'GRUPO3.CNV')),\
    #     # 'CODOCUPMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'GRUPO4.CNV')),\
    #     # 'CODOCUPMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'CBO2002.CNV')),\
    #     # 'CODOCUPMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'GRUPOCUP.CNV')),\
    #     # 'CODOCUPMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'OCUPA.CNV')),\
    #     'QTDFILVIVO':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'FILTIDO.CNV')),\
    #     'QTDFILMORT':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'FILTIDO.CNV')),\
    #     'CODMUNRES':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'MUNICBR.CNV')),\
    #     'GESTACAO':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'SEMANAS.CNV')),\
    #     'GRAVIDEZ':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'GRAVIDEZ.CNV')),\
    #     'PARTO':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'PARTO.CNV')),\
    #     'CONSULTAS':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'CONSULTA.CNV')),\
    #     # 'DTNASC':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'ANO.CNV')),\
    #     # 'DTNASC':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'MESES.CNV')),\
    #     'HORANASC':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'HORAOBITO.CNV')),\
    #     'SEXO':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'SEXO.CNV')),\
    #     'APGAR1':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'APGAR.CNV')),\
    #     'APGAR5':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'APGAR.CNV')),\
    #     'RACACOR':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'RACA.CNV')),\
    #     'PESO':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'PESO.CNV')),\
    #     'idanomal.cnv':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'idanomal.cnv')),\
    #     'DTCADASTRO':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'MESES.CNV')),\
    #     'CODANOMAL':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'CID1017.cnv')),\
    #     'NATURALMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'NATURAL.CNV')),\
    #     'CODMUNNATU':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'MUNICBR.CNV')),\
    #     'CODUFNATU':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'UFC.CNV')),\
    #     'ESCMAE2010':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'ESC2010.CNV')),\
    #     'SERIESCMAE':'Série escolar da mãe. Valores de 1 a 8.',\
    #     # 'RACACORMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'RACA.CNV')),\
    #     'QTDGESTANT':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'GESTANT.cnv')),\
    #     'QTDPARTNOR':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'PARTON.CNV')),\
    #     'QTDPARTCES':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'PARTON.CNV')),\
    #     'IDADEPAI':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'IDADEPAI.CNV')),\
    #     'DTULTMENST':'Data da última menstruação (DUM): dd mm aaaa',\
    #     'SEMAGESTAC':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'SEMADUM.CNV')),\
    #     'TPMETESTIM':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'TPMETODO.CNV')),\
    #     'CONSPRENAT':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'SEMADUM.CNV')),\
    #     'MESPRENAT':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'MEGEST.CNV')),\
    #     'TPAPRESENT':'Tipo de apresentação do RN. Valores: 1– Cefálico; 2– Pélvica oupodálica; 3– Transversa; 9– Ignorado',\
    #     'STTRABPART':'Trabalho de parto induzido? Valores: 1– Sim; 2– Não; 3– Não se aplica; 9– Ignorado',\
    #     'STCESPARTO':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'STPARTO.CNV')),\
    #     'TPNASCASSI':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'TPASSIST.CNV')),\
    #     'TPFUNCRESP':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'TPFUNC.CNV')),\
    #     'TPDOCRESP':'Tipo do documento do responsável. Valores: 1‐CNES; 2‐CRM; 3‐COREN; 4‐RG; 5‐CPF',\
    #     #'DTDECLARAC':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'.CNV')),\
    #     'ESCMAEAGR1':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'ESCAGR1.CNV')),\
    #     'STDNEPIDEM':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'DNNOVA.CNV')),\
    #     'STDNNOVA':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'DNNOVA.CNV')),\
    #     'CODPAISRES':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'PAISES.CNV')),\
    #     'TPROBSON':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'ROBSON.CNV')),\
    #     #'PARIDADE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'.CNV')),\
    #     #'KOTELCHUCK':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'.CNV')),\
    #     # 'DTRECEBIM':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'ANO.CNV')),\
    #     # 'DIFDATA':'Diferença entre a data de óbito e data do recebimento originalda DO ([DTNASC] – [DTRECORIG]) ',\
    #     # 'DTRECORIGA':'Data do 1º recebimento do lote, dada pelo Sisnet.',
    #     }
    #     return columns_variables_descriptions

    # def describe_columns(self,**kwargs):
    #     return self._columns_descriptions 




