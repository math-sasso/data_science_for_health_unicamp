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

class SINASC_Retriever(Retriever):
    def __init__(self):
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
        json_result = kwargs.get('json_path')
        
        #Removing Duplicates
        states = list(set(states))
        years = list(set(years))
        
        #Checking Errors
        check_inputs_erros(states,years)

        #Creating Json
        json_result = IO_Utils.read_json(json_path) if json_path else {'metadata': {'column_descriptions':{}}}
        for state in states:
            for year in years:
                df = download(state, year)
                #df = download('SE', 2015)
                json_result['data']['state']['year'] = df

                IO_Utils.read_json()
                IO_Utils.save_json()


        
    def _get_all_column_variables_descriptions(self):
        #TODO: Coletar as informaçõs de cada coluna
        columns = ['contador', 'ORIGEM', 'CODESTAB', 'CODMUNNASC', 'LOCNASC', 'IDADEMAE','ESTCIVMAE', 'ESCMAE', 'CODOCUPMAE', 'QTDFILVIVO', 'QTDFILMORT','CODMUNRES', 'GESTACAO', 'GRAVIDEZ', 'PARTO', 'CONSULTAS', 'DTNASC','HORANASC', 'SEXO', 'APGAR1', 'APGAR5', 'RACACOR', 'PESO', 'IDANOMAL','DTCADASTRO', 'CODANOMAL', 'NUMEROLOTE', 'VERSAOSIST', 'DTRECEBIM','DIFDATA', 'DTRECORIGA', 'NATURALMAE', 'CODMUNNATU', 'CODUFNATU','ESCMAE2010', 'SERIESCMAE', 'DTNASCMAE', 'RACACORMAE', 'QTDGESTANT','QTDPARTNOR', 'QTDPARTCES', 'IDADEPAI', 'DTULTMENST', 'SEMAGESTAC','TPMETESTIM', 'CONSPRENAT', 'MESPRENAT', 'TPAPRESENT', 'STTRABPART','STCESPARTO', 'TPNASCASSI', 'TPFUNCRESP', 'TPDOCRESP', 'DTDECLARAC','ESCMAEAGR1', 'STDNEPIDEM', 'STDNNOVA', 'CODPAISRES', 'TPROBSON','PARIDADE', 'KOTELCHUCK']
        #codigos municipios
        #https://www.anatel.gov.br/dadosabertos/PDA/Codigo_Nacional/PGCN.csv
        #https://bigdata-metadados.icict.fiocruz.br/dataset/sistema-de-informacoes-de-nascidos-vivos-sinasc/resource/9d664e65-2dbd-44cf-8f4a-65499affa27c
        #http://www2.datasus.gov.br/DATASUS/index.php?area=0901&item=1&acao=28
        #http://svs.aids.gov.br/dantps/cgiae/sinasc/documentacao/
        {'contador':'Numero linha do dataframe',
        'ORIGEM':}
        return 1
    
    def describe_data(self,**kwargs):
        return self._columns_descriptions 




