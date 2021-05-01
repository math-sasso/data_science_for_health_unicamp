from typing import List
from pysus.online_data.sinasc import download


class SINASC_Retriever(object):
    def __init__(self):
        self.columns_descriptions = self._get_all_column_variables_descriptions()
    def get_data(self,states:List[str],years:List[int]):
        
        #TODO: Checagem se o ano está fora do range
        #TODO: Checagem se as abreviações estão fora das opções
        def check_inputs_erros():
            pass
        df = download('SE', 2015)

    def _get_all_column_variables_descriptions(self):
        #TODO: Coletar as informaçõs de cada coluna
        return 1




