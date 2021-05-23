import warnings
import math
from copy import deepcopy
from typing import List,Tuple
import itertools
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import plotly.express as px

import sklearn
from sklearn import preprocessing
from sklearn.metrics import auc, roc_curve, accuracy_score, precision_recall_fscore_support,confusion_matrix
from sklearn.feature_selection import RFE
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from scipy.stats import gaussian_kde
from scipy.stats import probplot

class Visualizer(object):
    """ 
    Class with preprocessments to apply in dataframe
    """
    def __init__(self):
        super().__init__()
        self.loc_locale = "lower right"

    def _calculate_two_class_roc_curve(self, y_test: np.ndarray, y_prob: np.ndarray, labels: np.ndarray, ax: plt.Axes):
        """Plot a roc curve for a two class dataset.
        Args:
            y_test (np.ndarray): target split used for tests.
            y_pred (np.ndarray): probability of each y_test class according to the model.
            labels (np.ndarray): target labels.
            ax (matplotlib.Axes): axes from subplot
        Returns:
            (matplotlib.Axes): the axes object.
        """

        fpr, tpr, _ = roc_curve(y_test, y_prob[:, 1])
        roc_auc = auc(fpr, tpr)

        # Plot ROC Curve
        lw = 2
        ax.plot(
            fpr,
            tpr,
            color="darkorange",
            lw=lw,
            label="ROC curve (area = %0.2f)" % roc_auc,
        )
        
        return ax



    def _calculate_full_roc_curve(self,y_true: np.ndarray, y_prob: np.ndarray, labels: np.ndarray, ax: plt.Axes):
        """Plot a roc curve for all classes of the dataset.
        Args:
            y_true (np.ndarray): target split used for tests.
            y_prob (np.ndarray): probability of each y_true class according to the model.
            labels (np.ndarray): target labels.
            ax (matplotlib.Axes): axes from subplot
        Returns:
            (matplotlib.Axes): the axes object.
        """

        # Binarize the output
        lb = preprocessing.LabelBinarizer()
        y_true_bin = lb.fit_transform(y_true)

        # Compute ROC curve for each class
        fpr, tpr, roc_auc = {}, {}, {}

        used_y = list(set(y_true))
        for i in used_y:
            fpr[i], tpr[i], _ = roc_curve(y_true_bin[:, i], y_prob[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])

        color = cm.rainbow(np.linspace(0, 1, len(used_y) + 1))
        
        lw = 2
        for i, c in zip(used_y, color):
            ax.plot(
                fpr[i],
                tpr[i],
                color=c,
                lw=lw,
                label="Classe %s (area = %0.2f)" % (labels[i], roc_auc[i]),
            )

        return ax


    def plot_roc_curve(self,y_true: np.ndarray, y_prob: np.ndarray, labels: np.ndarray):
        """Plot a roc curve.
        Args:
            y_true (np.ndarray): target split used for tests.
            y_prob (np.ndarray): probability of each y_true class according to the model.
            labels (np.ndarray): target labels.
        Returns:
            (matplotlib.Axes): the axes object.
        """

        ax = plt.subplot()

        lw = 2
        ax.plot([0, 1], [0, 1], color="navy", lw=lw, linestyle="--")
        ax.set_xlim([-0.01, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel("Taxa de Falso Positivo")
        ax.set_ylabel("Taxa de Verdadeiro Positivo")
        ax.set_title("Curva ROC", fontweight='bold')

        if len(set(y_true)) == 2:
            ax = self._calculate_two_class_roc_curve(y_true, y_prob, labels, ax)
        else:
            ax = self._calculate_full_roc_curve(y_true, y_prob, labels, ax)

        ax.legend(loc=self.loc_locale)

        return ax


    def plot_confusion_matrix(self,y_true, y_pred,labels):
        title='Confusion matrix'
        cmap=plt.cm.Blues

        cm = confusion_matrix(y_true, y_pred,labels=labels)

        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

        plt.figure(figsize=(7,7))
        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title, fontsize=25)
        tick_marks = np.arange(len(labels))
        plt.xticks(tick_marks, labels, rotation=90, fontsize=15)
        plt.yticks(tick_marks, labels, fontsize=15)

        fmt = '.2f'
        thresh = cm.max() / 2.
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(j, i, format(cm[i, j], fmt),
                    horizontalalignment="center",
                    color="white" if cm[i, j] > thresh else "black", fontsize = 14)

        plt.ylabel('True label', fontsize=20)
        plt.xlabel('Predicted label', fontsize=20)
        plt.show()


    # def plot_matrix(self,data: pd.DataFrame):
    #     """Plots a confusion matrix.
    #     Args:
    #         data (pd.Dataframe): confusion matrix.
    #     Returns:
    #         (matplotlib.Axes): the axes object.
    #     """

    #     data.index.name = "Classes Verdadeiras"
    #     data.columns.name = "Classes Previstas"

    #     ax = sns.heatmap(data,
    #                     annot=True,
    #                     annot_kws={"fontsize": 14},
    #                     cbar=False,
    #                     cmap="Blues")

    #     ax.set_xlabel(data.columns.name, fontsize=16, rotation=0, labelpad=20)
    #     ax.set_ylabel(data.index.name, fontsize=16, labelpad=20)
    #     ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    #     ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    #     ax.xaxis.set_label_position("top")
    #     ax.xaxis.tick_top()
    #     plt.tight_layout()

    #     return ax
    
    # def plot_roc_curve(self,y_true, y_prob):
    #     """Plot a roc curve.
    #     Args:
    #         y_true (np.ndarray): target split used for tests.
    #         y_prob (np.ndarray): probability of each y_true class according to the model.
    #     Returns:
    #         (matplotlib.Axes): the axes object.
    #     """

    #     lr_probs = y_prob[:, 1]
    #     ns_probs = [0 for _ in range(len(lr_probs))]
    #     # calculate scores
    #     ns_auc = roc_auc_score(y_true, ns_probs)
    #     lr_auc = roc_auc_score(y_true, lr_probs)
    #     # summarize scores
    #     print('No Skill: ROC AUC=%.3f' % (ns_auc))
    #     print('Logistic: ROC AUC=%.3f' % (lr_auc))
    #     # calculate roc curves
    #     ns_fpr, ns_tpr, _ = roc_curve(y_true, ns_probs)
    #     lr_fpr, lr_tpr, _ = roc_curve(y_true, lr_probs)
    #     # plot the roc curve for the model
    #     plt.plot(ns_fpr, ns_tpr, linestyle='--', label='No Skill')
    #     plt.plot(lr_fpr, lr_tpr, marker='.', label='Logistic')
    #     # axis labels
    #     plt.xlabel('False Positive Rate')
    #     plt.ylabel('True Positive Rate')
    #     # show the legend
    #     plt.legend()
    #     # show the plot
    #     plt.show()