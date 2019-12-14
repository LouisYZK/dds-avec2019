"""Simple predictor using random forest
"""

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import f1_score
from sklearn.model_selection import cross_val_score
from sklearn import metrics

from core.predictor.predictor import Predictor
from common.sql_handler import SqlHandler
import config
from global_values import *

class RfPredictor(Predictor):
    def __init__(self, feature_table,
                 gender=False):
        pass


    def train(self):
        pass

    def predict(self):
        pass

    def metric_reslt(self):
        pass