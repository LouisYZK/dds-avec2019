"""
Gather training request from user and dispatch them
"""
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor, wait
from global_values import *
from common.log_handler import get_logger
logger = get_logger()


class Train(Process):
    def __init__(self, model_name=None,
                 feature_name=None,
                 gender=False):
        super().__init__()
        self.model_name =model_name
        self.feature_name = feature_name
        self.gender = gender
        self._set_feature()


    def _set_feature(self):
        if self.feature_name == FEATURE_EXP_2:
            # if choose exp2 the data will be in pandas's dataframe by defaut
            from common.df_handler import get_data_by_id
            self.data = get_data_by_id(config.tbl_exp2_audio_fea, self.gender)
        else:
            print('not finished yet')

    def _train_eval(self, train, dev, model):
        model = model(train, dev)
        model.train()
        return  model.eval()

    def run(self):
        if self.model_name == MODEL_RF:
            from core.predictor.RF.rf_predict import RfPredictor
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
                # with ThreadPoolExecutor() as executor:
                #     task1 = executor.submit(self._train_eval, train_m, dev_m, RfPredictor)
                #     task2 = executor.submit(self._train_eval, train_f, dev_f, RfPredictor)
                #     score1 = wait(task1)
                #     score2 = wait(task2)
                #     logger.info(f'Evalutaion Scores Male {self.model_name} with {self.feature_name}: {score1}')
                #     logger.info(f'Evalutaion Scores Female {self.model_name} with {self.feature_name}: {score2}')
                    
                    
        else:
            print('not finish yet!')