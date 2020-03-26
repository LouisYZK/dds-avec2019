"""Simple predictor using random forest
"""

import pandas as pd
import numpy as np
import math
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import f1_score
from sklearn.model_selection import cross_val_score
from sklearn import metrics

from core.predictor.predictor import Predictor
from common.sql_handler import SqlHandler
from common.metric import ccc_score
import config
from global_values import *
from common.log_handler import get_logger
logger = get_logger()

def pre_data(df):
    df[np.isnan(df)] = 0.0
    df[np.isinf(df)] = 0.0
    return df

class RfPredictor(Predictor):
    def __init__(self, train, dev, features=None):
        """
        Input:
            train and dev are ndarray-like data
            features are the freature name in tran and dev
        """
        self.train_set = pre_data(train)
        self.dev_set = pre_data(dev)
        self.feature_list = features

    def train(self):
        self.rf = RandomForestRegressor(n_estimators=100,
                                        criterion='mse',
                                        n_jobs=-1)
        X = self.train_set.loc[:, 'F0_mean':].values
        y = self.train_set['PHQ8_Score'].values.ravel()
        self.rf.fit(X, y)
        

    def predict(self, X):
        y = self.rf.predict(X)
        return y

    def eval(self):
        X = self.dev_set.loc[:, 'F0_mean':].values
        y = self.dev_set['PHQ8_Score'].values
        scores = cross_val_score(self.rf, X, y, cv=10, scoring='neg_mean_absolute_error') 
        mae = abs(scores.mean())

        scores = cross_val_score(self.rf, X, y, cv=10, scoring='neg_mean_squared_error') 
        rmse = math.sqrt(abs(scores.mean()))

        y_pred = self.predict(X)
        ccc = ccc_score(y, y_pred)
        
        fea_importance = self.rf.feature_importances_
        fea_imp_dct = {fea:val for fea, val in zip(self.feature_list, fea_importance)}
        top = sorted(fea_imp_dct, key=lambda x: fea_imp_dct[x], reverse=True)[:5]
        top_fea = {fea: fea_imp_dct[fea] for fea in top}
        
        return {'MAE': mae, 'RMSE': rmse, 'CCC':ccc, 'feature_importaces': top_fea}

class MultiModalRandomForest(Predictor):
    def __init__(self, data, features):
        """
        data and features is a dictionary that conatines data we need.
        """
        self.data = data
        self.features = features

    def train(self):
        pass

    def predict(self):
        pass

    def eval(self):
        pass