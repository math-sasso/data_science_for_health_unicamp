import os
import numpy as np
from typing import List
from pysus.online_data.sinasc import download
from io_utils import IO_Utils

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

        self.wordk_dir = os.getcwd().replace('= ','')
        self.data_dir = os.path.join(self.wordk_dir,'data')

        self.io_utils = IO_Utils()


class SINASC_Retriever(Retriever):
    def __init__(self):
        super().__init__()
        self._columns_descriptions = self._get_all_column_variables_descriptions()
        self.acceptable_years = np.arange(1999,2020)

    def get_data(self,**kwargs):
    
        def check_inputs_erros(states,years):
            if (type(years) != list) or not all(isinstance(i, int) for i in years):
                raise AttributeError("O argumento years deve ser uma lista de inteiros")
            
            if (type(years) != list) or not all(isinstance(i, str) for i in states):
                raise AttributeError("O argumento states deve ser uma lista de strings")

            if not set(years).issubset(self.acceptable_years):
                raise AttributeError("Todos os anos devem estar entre 1999 e 2019")
            
            if not set(states).issubset(self.states_brasil.keys()):
                raise AttributeError(f"Todos os estados devem estar na lista: {list(self.states_brasil.keys())}")
       
        states = kwargs.get('states')
        years = kwargs.get('years')
        json_path = kwargs.get('json_path',None)
        
        #Removing Duplicates
        states = list(set(states))
        years = list(set(years))
        
        #Checking Errors
        check_inputs_erros(states,years)

        #Creating Json
        json_result = self.io_utils.read_json(json_path) if json_path else {'metadata': {'column_descriptions':{}}}
        for state in states:
            for year in years:
                df = download(state, year)
                #df = download('SE', 2015)
                json_result['data']['state']['year'] = df

                self.io_utils.read_json()
                self.io_utils.save_json()


        
    def _get_all_column_variables_descriptions(self):
        #codigos municipios
        #https://www.anatel.gov.br/dadosabertos/PDA/Codigo_Nacional/PGCN.csv
        #https://bigdata-metadados.icict.fiocruz.br/dataset/sistema-de-informacoes-de-nascidos-vivos-sinasc/resource/9d664e65-2dbd-44cf-8f4a-65499affa27c
        #http://www2.datasus.gov.br/DATASUS/index.php?area=0901&item=1&acao=28
        #http://svs.aids.gov.br/dantps/cgiae/sinasc/documentacao/
        #TODO: Coletar as informaçõs de cada coluna
        tabdn_dir = os.path.join(self.data_dir,'raw','tabdn')
        jsons_tabdn_dir = os.path.join(self.data_dir,'raw','jsons_tabdn')
        columns_variables_descriptions = {'CODMUNNASC':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'MUNICBR.CNV'),columns=['codigo-cidade','codigos_aceitos','possivel_lixo']),\
        'LOCNASC':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'LOCOCOR.CNV')),\
        'IDADEMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'FXtabnet.cnv')),\
        'ESTCIVMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'ESTCIV.CNV')),\
        'ESCMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'INSTRUC.CNV')),\
        # 'CODOCUPMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'GRUPO1.CNV')),\
        # 'CODOCUPMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'GRUPO2.CNV')),\
        # 'CODOCUPMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'GRUPO3.CNV')),\
        # 'CODOCUPMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'GRUPO4.CNV')),\
        # 'CODOCUPMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'CBO2002.CNV')),\
        # 'CODOCUPMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'GRUPOCUP.CNV')),\
        # 'CODOCUPMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'OCUPA.CNV')),\
        'QTDFILVIVO':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'FILTIDO.CNV')),\
        'QTDFILMORT':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'FILTIDO.CNV')),\
        'CODMUNRES':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'MUNICBR.CNV')),\
        'GESTACAO':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'SEMANAS.CNV')),\
        'GRAVIDEZ':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'GRAVIDEZ.CNV')),\
        'PARTO':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'PARTO.CNV')),\
        'CONSULTAS':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'CONSULTA.CNV')),\
        # 'DTNASC':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'ANO.CNV')),\
        # 'DTNASC':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'MESES.CNV')),\
        'HORANASC':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'HORAOBITO.CNV')),\
        'SEXO':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'SEXO.CNV')),\
        'APGAR1':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'APGAR.CNV')),\
        'APGAR5':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'APGAR.CNV')),\
        'RACACOR':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'RACA.CNV')),\
        'PESO':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'PESO.CNV')),\
        'idanomal.cnv':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'idanomal.cnv')),\
        'DTCADASTRO':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'MESES.CNV')),\
        'CODANOMAL':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'CID1017.cnv')),\
        'NATURALMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'NATURAL.CNV')),\
        'CODMUNNATU':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'MUNICBR.CNV')),\
        'CODUFNATU':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'UFC.CNV')),\
        'ESCMAE2010':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'ESC2010.CNV')),\
        'SERIESCMAE':'Série escolar da mãe. Valores de 1 a 8.',\
        # 'RACACORMAE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'RACA.CNV')),\
        'QTDGESTANT':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'GESTANT.cnv')),\
        'QTDPARTNOR':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'PARTON.CNV')),\
        'QTDPARTCES':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'PARTON.CNV')),\
        'IDADEPAI':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'IDADEPAI.CNV')),\
        'DTULTMENST':'Data da última menstruação (DUM): dd mm aaaa',\
        'SEMAGESTAC':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'SEMADUM.CNV')),\
        'TPMETESTIM':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'TPMETODO.CNV')),\
        'CONSPRENAT':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'SEMADUM.CNV')),\
        'MESPRENAT':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'MEGEST.CNV')),\
        'TPAPRESENT':'Tipo de apresentação do RN. Valores: 1– Cefálico; 2– Pélvica oupodálica; 3– Transversa; 9– Ignorado',\
        'STTRABPART':'Trabalho de parto induzido? Valores: 1– Sim; 2– Não; 3– Não se aplica; 9– Ignorado',\
        'STCESPARTO':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'STPARTO.CNV ')),\
        'TPNASCASSI':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'TPASSIST.CNV')),\
        'TPFUNCRESP':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'TPFUNC.CNV')),\
        'TPDOCRESP':'Tipo do documento do responsável. Valores: 1‐CNES; 2‐CRM; 3‐COREN; 4‐RG; 5‐CPF',\
        #'DTDECLARAC':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'.CNV')),\
        'ESCMAEAGR1':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'ESCAGR1.CNV')),\
        'STDNEPIDEM':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'DNNOVA.CNV')),\
        'STDNNOVA':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'DNNOVA.CNV')),\
        'CODPAISRES':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'PAISES.CNV.CNV')),\
        'TPROBSON':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'ROBSON.CNV')),\
        'PARIDADE':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'.CNV')),\
        'KOTELCHUCK':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'.CNV')),\
        # 'DTRECEBIM':self.io_utils.read_cnv_file_as_df(os.path.join(tabdn_dir,'ANO.CNV')),\
        # 'DIFDATA':'Diferença entre a data de óbito e data do recebimento originalda DO ([DTNASC] – [DTRECORIG]) ',\
        # 'DTRECORIGA':'Data do 1º recebimento do lote, dada pelo Sisnet.',
        }
        return columns_variables_descriptions
    
    def describe_columns(self,**kwargs):
        return self._columns_descriptions 




