import os
import pandas as pd
import pdb
import seaborn as sns
import matplotlib.pyplot as plt
import pymrmr
from scipy.stats import kendalltau, pearsonr, spearmanr
from sklearn.feature_selection import SelectKBest, mutual_info_classif, chi2, f_classif, RFE
import numpy as np

# Feature Importance Sklearn
# https://machinelearningmastery.com/calculate-feature-importance-with-python/

class Feature_Selection(object):
    """ 
    Class with preprocessments to apply in dataframe
    """
    def __init__(self):
        super().__init__()
        self.correlation_matrix = Correlation_Matrix()

    def select_features(self,df,columns):
        raise NotImplementedError()

    def _split_df_in_xy(self,df,target_column):
        df_copy = df.copy()
        X = df_copy.drop(target_column,axis = 1)
        y = df_copy[target_column]
        return X,y

    def get_missing_values_df(self,df):
        percent_missing = df.isnull().sum() * 100 / len(df)
        missing_value_df = pd.DataFrame({'column_name': df.columns,'percent_missing': percent_missing})
        return missing_value_df

    def get_correlation_matrix(self,df,method):
        return self.correlation_matrix.get_correlation_matrix(df,method)

    def plot_correlation_matrix(self,df_corr,plot=True):
        return self.correlation_matrix.plot_correlation_matrix(df_corr,plot)
    
    def get_correlation_with_target(self,df,target_column,method,num_feats=10):
        return self.correlation_matrix.get_correlation_with_target(df,target_column,method,num_feats)
    
    def get_IG_feature_scores(self,df,n_features_to_select):
        """
        IG calculates the importance of each feature by measuring the increase in entropy when the feature is given vs. absent.
        """
        bestfeatures = SelectKBest(score_func=mutual_info_classif, k=n_features_to_select) # n is number of features you want to select
        fit = bestfeatures.fit(xs,y)
        dfscores = pd.DataFrame(fit.scores_)
        dfcolumns = pd.DataFrame(xs.columns)
        featureScores = pd.concat([dfcolumns,dfscores],axis=1)
        featureScores.columns = ['Feature','Score']
        return featureScores
                 
    def get_mRMR_feature_scores(self,df,n_features_to_select):
        # https://medium.com/subex-ai-labs/feature-selection-techniques-for-machine-learning-in-python-455dadcd3869
        """
        (Minimal Redundancy and Maximal Relevance)
        Intuition: It selects the features, based on their relevancy with the target variable, as well as their redundancy with the other features.
        """
        selected_features = pymrmr.mRMR(df, 'MIQ',n_features_to_select)
        return selected_features

    def get_chisquare_feature_scores(self,df,target_column,n_features_to_select):
        """
        It calculates the correlation between the feature and target and selects the best k features according to their chi square score calculated using following chi square test.
        """
        X,y = self._split_df_in_xy(df,target_column)
        import pdb;pdb.set_trace()
        bestfeatures = SelectKBest(score_func=chi2, k=n_features_to_select) # n is number of features you want to select
        fit = bestfeatures.fit(X,y)
        dfscores = pd.DataFrame(fit.scores_)
        dfcolumns = pd.DataFrame(xs.columns)
        featureScores = pd.concat([dfcolumns,dfscores],axis=1)
        featureScores.columns = ['Feature','Score']
        return featureScores

    def get_anova_feature_scores(self,df,n_features_to_select):
        """
        We perform Anova between features and target to check if they belong to same population.
        """
        bestfeatures = SelectKBest(score_func=f_classif, k=n_features_to_select) # n is number of features you want to select
        fit = bestfeatures.fit(xs,y)
        dfscores = pd.DataFrame(fit.scores_)
        dfcolumns = pd.DataFrame(xs.columns)
        featureScores = pd.concat([dfcolumns,dfscores],axis=1)
        featureScores.columns = ['Feature','Score']
        return featureScores

    def get_features_by_RFE(self,df,model):
        """
         It is a greedy optimization algorithm which aims to find the best performing feature subset. It repeatedly creates models and keeps aside the best or the worst performing feature at each iteration. It constructs the next model with the left features until all the features are exhausted. It then ranks the features based on the order of their elimination.
        """
        #model = LogisticRegression(max_iter=1000)
        rfe_model = RFE(model, 20)
        rfe_fit = rfe_model.fit(x, y)
        selected = df[df.columns[rfe_fit.get_support(indices=True)]]
        return selected

    def get_feature_selection_summary(self,df):
        # https://towardsdatascience.com/the-5-feature-selection-algorithms-every-data-scientist-need-to-know-3a6b566efd2
        # put all selection together
        feature_selection_df = pd.DataFrame({'Feature':feature_name, 'Pearson':cor_support, 'Chi-2':chi_support, 'RFE':rfe_support, 'Logistics':embeded_lr_support,
                                            'Random Forest':embeded_rf_support, 'LightGBM':embeded_lgb_support})
        # count the selected times for each feature
        feature_selection_df['Total'] = np.sum(feature_selection_df, axis=1)
        # display the top 100
        feature_selection_df = feature_selection_df.sort_values(['Total','Feature'] , ascending=False)
        feature_selection_df.index = range(1, len(feature_selection_df)+1)
        feature_selection_df.head(num_feats)

    
class Correlation_Matrix(object):

    def __init__(self):
        super().__init__()

    def get_correlation_with_target(self,df,target_column,method,num_feats):
        corr_dict = self.get_correlation_matrix(df,method)
        df_k,df_p = corr_dict['df_k'],corr_dict['df_p']
        correlations_with_target = df_k[target_column]
        correlations_with_target = correlations_with_target.fillna(0)
        correlations_with_target = correlations_with_target[correlations_with_target.index.difference([target_column])]
        correlations_with_target = correlations_with_target.map(lambda x : x).abs().sort_values(ascending = False)
        correlations_with_target = correlations_with_target[:num_feats]
        return correlations_with_target
    
    def plot_correlation_matrix(self,df_corr,plot=True):
        plt.figure(figsize=(16, 6))
        heatmap = sns.heatmap(df_corr, vmin=-1, vmax=1, annot=True, cmap='coolwarm')
        heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':18}, pad=12)
        if plot:
            plt.show()
        else:
            return heatmap

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
        
        df_k = df.corr(method=method_k)
        df_p = df.corr(method=method_p)
    
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
    
    