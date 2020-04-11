import os
import numpy as np
import pandas as pd
import scipy.stats

"""
'frame', 'face_id', 'timestamp', 'confidence','success',
gaze_0_(x,y,z), gaze_1_(x,y,z), gaze_angle_x, gaze_angle_y,
eye_lmk_(x,y)_(0,55), ege_lmk_(X,Y,Z)_(0,55)
pose_(Tx, Ty, Tz), pose_(Rx, Ry, Rz)
x_(0, 67), y(0,67), (X,Y,Z)_(0,67)
p_(rx, ry, rz), p(tx, ty), p_(0, 33)
AU
"""
video_dir = '/home/yzk/data/finance_mv'
lld_dir = '/home/yzk/data/mv_llds'
label_dir = '/home/yzk/data/fin_labels.csv'

video_ids = [item.split('.')[0] for item in os.listdir(video_dir)]

def handler_col(df):
    index = df.columns.tolist()
    df.columns = [item.strip() for item in index]
    return df

class StatsFea():
    def __init__(self, dataframe):
        self.columns = ['mean', 'std', 'skew', 'iqr', 'spectral']
        self.df = dataframe
        cols = self.df.columns.tolist()
        self.feature_name = []
        for col, s_fea in zip(cols, self.columns):
            self.feature_name.append(f'{col}_{s_fea}')

    def _gen_fea(self, data):
        """Assume data is a one-dimentional vector
        """
        stats_fea = list()
        stats_fea.append(np.mean(data))
        stats_fea.append(np.std(data))
        stats_fea.append(scipy.stats.skew(data))
        stats_fea.append(scipy.stats.iqr(data)) # interquantile range)
        stats_fea.append(scipy.stats.gmean(data)/np.mean(data)) # spectral)
        return stats_fea
    
    def get_static_values(self):
        cols = self.df.columns.tolist()
        res = []
        for col in cols:
            stats_fea = self._gen_fea(self.df[col].values)
            res += stats_fea
        res = np.array(res)
        res[np.isnan(res)] = 0
        return res