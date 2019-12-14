"""
merge two dataframe according to ID to generate training and dev set;
"""
from common.sql_handler import SqlHandler
import config

def get_data_by_id(feature_table, gender=False):

    sql_handler = SqlHandler()
    feature = sql_handler.get_df(feature_table)
    feature['ID'] = feature['ID'].apply(pd.to_numeric)
    train = sql_handler.get_df(config.tbl_training_set)
    dev = sql_handler.get_df(config.tbl_develop_set)
    if not gender:
        train_set = pd.merge(train, feature, 
                                left_on='Participant_ID', right_on='ID')
        dev_set = pd.merge(dev, feature, 
                                left_on='Participant_ID', right_on='ID')

        return train_set, dev_set
    else:
        train_male = train[train['Gender'] == 1]
        train_female = train[train['Gender'] == 0]
        dev_male = train[train['Gender'] == 1]
        dev_female = train[train['Gender'] == 0]
        train_male = pd.merge(train_male, feature, 
                                    left_on='Participant_ID', right_on='ID')
        train_female = pd.merge(train_female, feature, 
                                    left_on='Participant_ID', right_on='ID')
        dev_male = pd.merge(dev_male, feature, 
                                left_on='Participant_ID', right_on='ID')
        dev_female = pd.merge(dev_female, feature, 
                                    left_on='Participant_ID', right_on='ID')
        return train_male, dev_male, train_female, dev_female