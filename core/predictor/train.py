"""
Gather training request from user and dispatch them
"""
from multiprocessing import Process
from global_values import *
class Train(Process):
    def __init__(self, model_name=None,
                 feature_name=None,
                 gender=False):
        self.model_name =model_name
        self.feature_name = feature_name
        self.gender = gender
        self._set_feature()


    def _set_feature(self):
        if self.feature_name == FEATURE_EXP_2:
            from common.df_handler import get_data_by_id
            self.data = get_data_by_id(config.tbl_exp2_audio_fea, gender)
        else:
            print('not finished yet')
    def run(self):
        if self.model_name == MODEL_RF:
            from core.predictor.RF.rf_predict import RfPredictor
            model = RfPredictor(self.data)
            pass
        else:
            print('not finish yet!')