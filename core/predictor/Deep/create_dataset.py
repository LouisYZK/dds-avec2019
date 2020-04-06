import pandas as pd
import numpy as np
import torch
from torch.utils.data import IterableDataset, DataLoader

import config
from common.sql_handler import SqlHandler
config.init()


class UnimodalDataset(IterableDataset):
    def __init__(self, feature_type, ids, random_crop=True):
        super().__init__()
        self.ids = ids
        self.random_crop = random_crop

        self.sql_handler = SqlHandler(type='sqlite')
        train_set = self.sql_handler.get_df(config.tbl_training_set)
        val_set = self.sql_handler.get_df(config.tbl_develop_set)
        self.dataset = pd.concat([train_set, val_set], axis=0)

        if feature_type == 'mfcc':
            self.table_name = config.tbl_mfcc
        elif feature_type == 'egemaps':
            self.table_name = config.tbl_egemaps
        elif feature_type == 'pose_gaze_faus':
            self.table_name = config.tbl_pose_gaze_faus

    def __del__(self):
        self.sql_handler.disconnect()

    def _get_feature(self, id):
        """get feature data according to id
        """
        max_length = config.max_sequence_num
        sql = f"select * from {self.table_name} where substr(name, 2,3)='{id}' limit {max_length}"
        feature_data = self.sql_handler.get_df(sql=sql).values[:, 2:]
        feature_data = feature_data.astype(np.float32)
        return feature_data

    def _get_label(self, id):
        assert type(id) == int
        score = self.dataset[self.dataset['Participant_ID'] == id]['PHQ8_Score'].values
        return score

    def _crop_feature(self, item):
        pass

    def _data_generator(self):
        for uid in self.ids:
            item, label = self._get_feature(uid), self._get_label(uid)
            if item.shape[0] == 0:
                continue
            yield item, label

    def __iter__(self):
        return self._data_generator()

def get_loader(feature_type, dataset_type='train'):
    sql_handler = SqlHandler()
    if dataset_type == 'train':
        ids = sql_handler.get_df(config.tbl_training_set)['Participant_ID'].tolist()
    elif dataset_type == 'valid':
        ids = sql_handler.get_df(config.tbl_develop_set)['Participant_ID'].tolist()
    else:
        ids = []
    dataset = UnimodalDataset(feature_type, ids)
    return DataLoader(dataset, batch_size=config.bacth_size, 
                      num_workers=config.wokers_num)