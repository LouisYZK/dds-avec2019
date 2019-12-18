"""
Gather training request from user and dispatch them
"""
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor, wait
from global_values import *
from common.df_handler import get_data_by_id, get_data_multi_modality
from common.sql_handler import SqlHandler
from common.log_handler import get_logger
logger = get_logger()


class Train(Process):
    def __init__(self, model_name=None,
                 feature_name=None,
                 gender=False,
                 feature_tables=None):
        """Train model Controller, dispatch the training tasks;
        Input:
            model_name: certain model depend on papers
            feature_name: support for a group of absolute features
            feature_tables: support for different feature table, which make it
                            is possible for us to combine different modality
                            features freely. But note that the train controller
                            is not responsible for processing the feature table,
                            it should be completed by a certain model.
            gender: if the model should consider the gender difference

        Output:
            Result and realted information will be printed by each estimator in logs'
        """
        super().__init__()
        self.model_name =model_name
        self.feature_name = feature_name
        self.feature_tables = feature_tables
        self.gender = gender
        self.sql_handler = SqlHandler()
        self._set_feature()


    def _set_feature(self):
        if self.feature_name is not None:
            # you r using feature from a ceratin way! 
            if self.feature_name == FEATURE_EXP_2:
                # if choose exp2 the data will be in pandas's dataframe by defaut
                self.data = get_data_by_id(config.tbl_exp2_audio_fea, self.gender)
                self.feature_list = self.sql_handler.get_cloumns_from_table(config.tbl_exp2_audio_fea)
                self.feature_list.remove('ID')
            else:
                print('not finished yet')
        elif self.feature_tables is not None:
            # Now you r using a multi-modality model!
            self.audio_data, self.video_data, self.text_data = \
                        get_data_multi_modality(self.feature_tables)
            self.audio_fea, self.video_fea, self.text_fea = \
                        self.sql_handler.get_cloumns_from_table(self.feature_tables)
        else:
            print('You must choose a set of features to train!!!')

    def _train_eval(self, train, dev, model):
        model = model(train, dev, features=self.feature_list)
        model.train()
        return  model.eval()

    def run(self):
        if self.model_name == MODEL_RF:
            from core.predictor.RF.rf_predict import RfPredictor
            if self.feature_name is not None:
                if not self.gender:
                    train, dev = self.data
                    score = self._train_eval(train, dev, RfPredictor)
                    logger.info(f'Evalutaion Scores {self.model_name} with {self.feature_name}: {score}')
                    
                else:
                    train_m, dev_m, train_f, dev_f = self.data
                    score = self._train_eval(train_m, dev_m, RfPredictor)
                    logger.info(f'Evalutaion Scores Male {self.model_name} with {self.feature_name}: {score}')

                    score = self._train_eval(train_f, dev_f, RfPredictor)
                    logger.info(f'Evalutaion Scores Female {self.model_name} with {self.feature_name}: {score}')
            else:
                if not self.gender:
                                        
                    
        else:
            print('not finish yet!')