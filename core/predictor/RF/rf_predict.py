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
    def __init__(self, train, dev):
        self.train_set = pre_data(train)
        self.dev_set = pre_data(dev)

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
        logger.info(f'final result: (MAE) {abs(scores.mean())}')

        scores = cross_val_score(self.rf, X, y, cv=10, scoring='neg_mean_squared_error') 
        logger.info(f'final result: (RMSE) {math.sqrt(abs(scores.mean()))}')

        y_pred = self.predict(X)
        print(y_pred)
        print(y)
        ccc = ccc_score(y, y_pred)
        logger.info(f'final result: (CCC) {ccc}')