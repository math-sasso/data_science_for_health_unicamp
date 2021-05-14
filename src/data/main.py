from retrievers import SINASC_Retriever
import numpy as np

retriever = SINASC_Retriever()
retriever.get_data(states=['SP'],years=np.arange(2009,2020).tolist())
