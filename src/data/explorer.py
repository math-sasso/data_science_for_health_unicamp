import pandas as pd
import numpy as np
import seaborn as sns
from scipy.stats import kendalltau, pearsonr, spearmanr

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
    
    def get_correlation_matrix(self,df,method):

        accpedted_correlations = ['pearson','spearman','kendall']
        if method not in accpedted_correlations:
            raise ValueError(f"O método deve ser um entre {accpedted_correlations}")

        if method == 'pearson':
            method_k = self._pearsonr_rval
            method_p = self._pearsonr_pval
        elif method == 'spearman':
            method_k = self._spearmanr_rval
            method_p = self._spearmanr_pval 
        elif method == 'kendall':
            method_k = self._kendall_rval
            method_p = self._kendall_pval

        df_k = df.corr(method=method_k).style.applymap(self._color_k)
        df_p = df.corr(method=method_p).style.applymap(self._color_p)
    
        return {'df_k':df_k,'df_p':df_p}

    def _kendall_rval(self,x,y):
        return np.round(kendalltau(x,y)[0],6)

    def _pearsonr_rval(self,x,y):
        return np.round(pearsonr(x,y)[0],6)

    def _spearmanr_rval(self,x,y):
        return np.round(spearmanr(x,y)[0],6)

    def _kendall_pval(self,x,y):
        return np.round(kendalltau(x,y)[1],6)

    def _pearsonr_pval(self,x,y):
        return np.round(pearsonr(x,y)[1],6)

    def _spearmanr_pval(self,x,y):
        return np.round(spearmanr(x,y)[1],6)
    
    def _color_k(self,value):
        value = abs(value)
        if value >=0.7 and  value <1:
            color = 'blue'
        elif value >=0.5 and value <0.7:
            color = 'green'
        elif value >=0.3 and value <0.5:
            color = 'red'
        else:
            color = ''
        return 'color: %s' % color
    
    def _color_p(self,value):
        if value <=0.001:
            color = 'blue'
        elif value <=0.05 and value >0.001:
            color = 'green'
        elif value <=0.1 and value >0.05:
            color = 'red'
        else:
            color = ''
        return 'color: %s' % color

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