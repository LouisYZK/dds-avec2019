"""
Face features extracted according to the paper
"""
import pandas as pd
from global_values import *
import config
from common.file_handler import gen_file_path_by_fea
from common.stats_features import StatsFea

class VideoFea(object):
    def __init__(self):
        self.sf = StatsFea()

    def gen_head_fea(self):
        folds = gen_file_path_by_fea('pose')
        feas = []
        for file in folds:
            fea_item = []
            ID = file[:3]; fea_item.append(ID)
            df_pose = pd.read_csv(file, header=0)
            col = df_pose.columns.values
            col = [item.strip() for item in col]
            df_pose.columns = col
            df_pose = df_pose.loc[:, 'Tx':]
            col = df_pose.columns.values
            for fea in col:
                fea_item += self.sf.gen_fea(df_pose[fea].values)
            feas.append(fea_item)

    def gen_face_fea(self):
        pass


    def to_db(self):
        pass
