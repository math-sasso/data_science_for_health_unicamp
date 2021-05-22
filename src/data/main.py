from retrievers import SINASC_Retriever
import numpy as np

retriever = SINASC_Retriever()
retriever.get_data(states=['SP','RJ','MG','ES'],years=np.arange(2010,2020).tolist())
