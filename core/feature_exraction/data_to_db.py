"""
Features reffered to paper:
Detect depression from communication: how computer vision, signal processing, and sentiment
analysis join forces
Aven Samareh, Yan Jin, Zhangyang Wang, Xiangyu Chang & Shuai Huang
"""
"""extract origin training set data or feature data into sqlite db;
"""

import pandas as pd
from sqlalchemy import create_engine, MetaData
import config

import global_values
from common.sql_handler import SqlHandler
import common.log_handler as log_handler

logger = log_handler.get_logger()

def data_set():
    df_train = pd.read_csv(config.data_dir + global_values.TRAIN_SET_NAME, header=0)
    df_dev = pd.read_csv(config.data_dir + global_values.DEL_SET_NAME, header=0)
    
    logger.debug(df_dev.head())
    sql_handler = SqlHandler()
    sql_handler.execute(f'drop table {config.tbl_develop_set}')
    sql_handler.execute(f'drop table {config.tbl_training_set}')

    sql_handler.df_to_db(df_train, config.tbl_training_set)
    sql_handler.df_to_db(df_dev, config.tbl_develop_set)



if __name__ == '__main__':
    data_set()
