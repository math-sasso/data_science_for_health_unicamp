import pandas as pd
import numpy as np
import seaborn as sns

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
        super().__init__()
    
    def get_unique_column_values(self,df):
        dic_uniques = {col: df[col].unique() for col in df.columns}
        return dic_uniques

    def descripe_dataframe(self,df):
        raise NotImplementedError()

class GraphExplorer(object):
    """ 
    Explore data from dataframes with graphs
    """
    def __init__(self):
        super().__init__()

    
    def get_histrogram(self,df,specific_columns=None):
        """
        Returns histograms for all the columns or only for the specified
        """
        raise NotImplementedError()

    def get_pca_graphs(self,df,specific_columns=None):
        """
        Returns PCA considering columns or only the specified
        """
        raise NotImplementedError()

    def get_scatter_plot_between_columns(self,df,specific_columns=None):
        """
        Returns PCA considering columns or only the specified
        """
        raise NotImplementedError()

    def get_violin_plot(self,df,specific_columns=None):
        """
        Returns violin plot
        """
        raise NotImplementedError()

    def get_correlation_graphs(self,df):
        """
        Get correlation kernels, scatter_plots and histograms considering variables
        """
        g = sns.PairGrid(df, palette="Set2")
        g.map_upper(sns.scatterplot)
        g.map_lower(sns.kdeplot)
        g.map_diag(sns.histplot)
        return g

    def get_correlation_graphs_for_categorical_variable(self,df,column):
        """
        Get correlation kernels, scatter_plots and histograms considering an spcefic variable
        """
        g = sns.PairGrid(df,hue=column, palette="Set2")
        g.map_upper(sns.scatterplot)
        g.map_lower(sns.kdeplot)
        g.map_diag(sns.histplot)
        g = g.add_legend()
        return g