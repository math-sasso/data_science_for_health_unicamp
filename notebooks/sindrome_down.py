import os
import sys
import pandas as pd
import pdb
import seaborn as sns
import matplotlib.pyplot as plt
sys.path.append(os.path.join(os.path.abspath(os.getcwd()),'..'))
from src.features.feature_selection import Feature_Selection
from src.features.feature_engineering import Feature_Engineering

target_anomal = 'Q909'


