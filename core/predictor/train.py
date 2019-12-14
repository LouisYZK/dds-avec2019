"""
Gather training request from user and dispatch them
"""
from multiprocessing import Process
from global_values import *
class Train(Process):
    def __init__(self, model_name=None,
                 feature_name=None):
        self.model_name =model_name

    def _get_feature(self):
        pass

    def run(self):
        if self.model_name == MODEL_RF:
            from core.predictor.RF.rf_predict import RfPredictor
            model = RfPredictor()
            pass
        else:
            print('not finish yet!')