class Explorer(object):
    """ 
    Explore data from dataframes
    """
    def __init__(self):
        pass

class StatisticalExplorer(object):
    """ 
    Explore statistics from data from dataframes
    """
    def __init__(self):
        pass
    
    def get_unique_column_values(self,df):
        dic_uniques = {col: df[col].unique() for col in df.columns}

        return dic_uniques
class GraphExplorer(object):
    """ 
    Explore data from dataframes with graphs
    """
    def __init__(self):
        pass