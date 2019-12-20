"""
merge two dataframe according to ID to generate training and dev set;
"""

import pandas as pd
from common.sql_handler import SqlHandler
import config
from global_values import *
from common.log_handler import get_logger
logger = get_logger()

def merge_df_by_id(df1, df2): 
    if df1 is None or df2 is None:
        return None
    return pd.merge(df1, df2, left_on='Participant_ID',
                                              right_on='ID')

def merge_dfs_by_id(dfs):
    if not dfs:
        logger.info('dfs is empty, which means one of the modality is None')
        return None
    if len(dfs) == 1:
        return dfs[0]
    else:
        merged_df = dfs[0]
        for df in dfs[1:]:
            # the common column is ID
            merged_df = pd.merge(merged_df, df)
        return merged_df

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


def get_data_multi_modality(tables, gender=False):
    """gather data from different tables in every modality
        and generate train set and dev dev set of them.
    """
    sql_handler = SqlHandler()
    audio_df, video_df, text_df = [], [], []
    for tb in tables:
        if tb in AUDIO_TABLE: audio_df.append(sql_handler.get_df(tb))
        elif tb in VIDEO_TABLE: video_df.append(sql_handler.get_df(tb))
        elif tb in TEXT_TABLE: text_df.append(sql_handler.get_df(tb))
        else: pass

    audio_merge_df = merge_dfs_by_id(audio_df)
    video_merge_df = merge_dfs_by_id(video_df)
    text_merge_df = merge_dfs_by_id(text_df)

    if not gender:
        train = sql_handler.get_df(config.tbl_training_set)
        dev = sql_handler.get_df(config.tbl_develop_set)
        
        data_dct = {
            'audio_train': merge_df_by_id(train, audio_merge_df),
            'audio_dev': merge_df_by_id(dev, audio_merge_df),
            'video_train': merge_df_by_id(train, video_merge_df),
            'video_dev': merge_df_by_id(dev, video_merge_df),
            'text_train': merge_df_by_id(train, text_merge_df),
            'text_dev': merge_df_by_id(dev, text_merge_df)
        }
    else:
        train_male = train[train['Gender'] == 1]
        train_female = train[train['Gender'] == 0]
        dev_male = train[train['Gender'] == 1]
        dev_female = train[train['Gender'] == 0]

        data_dct = {
            'male': {
                'audio_train': merge_df_by_id(train_male, audio_merge_df),
                'audio_dev': merge_df_by_id(dev_male, audio_merge_df),
                'video_train': merge_df_by_id(train_male, video_merge_df),
                'video_dev': merge_df_by_id(dev_male, video_merge_df),
                'text_train': merge_df_by_id(train_male, text_merge_df),
                'text_dev': merge_df_by_id(dev_male, text_merge_df)
            },
            'feamale':{
                'audio_train': merge_df_by_id(train_female, audio_merge_df),
                'audio_dev': merge_df_by_id(dev_female, audio_merge_df),
                'video_train': merge_df_by_id(train_female, video_merge_df),
                'video_dev': merge_df_by_id(dev_female, video_merge_df),
                'text_train': merge_df_by_id(train_female, text_merge_df),
                'text_dev': merge_df_by_id(dev_female, text_merge_df)
            }
        }
     

    return data_dct
        
