"""
Features reffered to paper:
Detect depression from communication: how computer vision, signal processing, and sentiment
analysis join forces
Aven Samareh, Yan Jin, Zhangyang Wang, Xiangyu Chang & Shuai Huang
"""
import pandas as pd
from sqlalchemy import create_engine, MetaData
import config

import global_values
from common.sql_handler import SqlHandler
import common.log_handler as log_handler

logger = log_handler.get_logger()

def data_set():
    engine = create_engine(f'sqlite:///{config.db_path}')
    df_train = pd.read_csv(config.data_dir + global_values.TRAIN_SET_NAME, header=0)
    df_dev = pd.read_csv(config.data_dir + global_values.DEL_SET_NAME, header=0)
    
    logger.debug(df_dev.head())
    sql_handler = SqlHandler()
    sql_handler.execute(f'drop table {config.tbl_develop_set}')
    sql_handler.execute(f'drop table {config.tbl_training_set}')
    df_train.to_sql(config.tbl_training_set, engine, index=False)
    df_dev.to_sql(config.tbl_develop_set, engine, index=False)


if __name__ == '__main__':
    data_set()