"""
merge two dataframe according to ID to generate training and dev set;
"""

import pandas as pd
from common.sql_handler import SqlHandler
import config
from global_values import *


def merge_df_by_id(df1, df2): 
    return pd.merge(df1, df2, left_on='Participant_ID',
                                              right_on='ID')

def get_data_by_id(feature_table, gender=False):

    sql_handler = SqlHandler()
    feature = sql_handler.get_df(feature_table)
    feature['ID'] = feature['ID'].apply(pd.to_numeric)
    train = sql_handler.get_df(config.tbl_training_set)
    dev = sql_handler.get_df(config.tbl_develop_set)
    if not gender:
        train_set = merge_df_by_id(train, feature)
        dev_set = merge_df_by_id(dev, feature)
        return train_set, dev_set
    else:
        train_male = train[train['Gender'] == 1]
        train_female = train[train['Gender'] == 0]
        dev_male = train[train['Gender'] == 1]
        dev_female = train[train['Gender'] == 0]
        
        train_male = merge_df_by_id(train_male, feature)
        train_female = merge_df_by_id(train_female, feature)
        dev_male = merge_df_by_id(dev_male, feature)
        dev_female = merge_df_by_id(dev_female, feature)
        return train_male, dev_male, train_female, dev_female


def get_data_multi_modality(tables):
    """gather data from different tables in every modality
        and generate train set and dev dev set of them.
    """
    sql_handler = SqlHandler()
    train = sql_handler.get_df(config.tbl_training_set)
    dev = sql_handler.get_df(config.tbl_develop_set)
    for tb in tables:
        pass
        
