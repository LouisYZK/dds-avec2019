import os
import torch
import config
import numpy as np
import pandas as pd


class FaceStatsDataset(torch.utils.data.IterableDataset):
    def __init__(self, feature_columns=None):
        super().__init__()
        data = []
        self.label = []
        df_label = pd.read_csv(config.label_dir)
        df_label['id'] = df_label['id'].apply(lambda x: x.strip())
        for video in config.video_ids:
            file_path = f'{config.lld_dir}/{video}/{video}.csv'
            if not os.path.exists(file_path): continue
            df = pd.read_csv(file_path)
            df = config.handler_col(df)
            df = df[(df.face_id==0) & (df.success==1)]
            df = df.loc[:, feature_columns]
            stat = config.StatsFea(df)
            data.append(stat.get_static_values())
            self.label.append(df_label[df_label.id==video]['label'].values)
        self.data = np.vstack(data)
        
    def __getitem__(self, ind):
        return self.data[ind], self.label[ind]
    def __len__(self):
        return self.data.shape[0]