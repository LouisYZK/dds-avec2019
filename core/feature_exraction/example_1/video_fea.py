"""
Face features extracted according to the paper
"""
import pandas as pd
import itertools
from concurrent.futures import ThreadPoolExecutor, as_completed
from global_values import *
import config
from common.file_handler import gen_file_path_by_fea
from common.stats_features import StatsFea
from common.sql_handler import SqlHandler
from common.log_handler import get_logger
logger = get_logger()


class VideoFea(object):
    def __init__(self):
        self.sf = StatsFea()
        self.head_fea_val = list()
        self.face_fea_val = list()
        
        self.head_fea = list(); self.head_fea.append('ID')
        self.head_fea += [fea + '_' + s_fea
            for fea, s_fea in itertools.product(POSE_COLUMNS, self.sf.columns)]

        self.face_fea = list(); self.face_fea.append('ID')
        self.face_fea += [fea + '_' + s_fea
            for fea, s_fea in itertools.product(EXP1_FACE_COLUMNS, self.sf.columns)]

    def _get_single_head_fea(self, file):
        fea_item = []
        ID = file.split('/')[-1][:3]; fea_item.append(ID)
        df_pose = pd.read_csv(file, header=0)
        col = df_pose.columns.values
        col = [item.strip() for item in col]
        df_pose.columns = col
        df_pose = df_pose.loc[:, 'Tx':]
        col = df_pose.columns.values
        for fea in col:
            fea_item += self.sf.gen_fea(df_pose[fea].values)
        
        self.head_fea_val.append(fea_item)
        logger.info(f'[fatures generation:] {ID} has extracted video head_fea in exp1!..')

    def gen_head_fea(self):
        folds = gen_file_path_by_fea('pose')
        with ThreadPoolExecutor() as executor:
            tasks = []
            for file in folds:
                f = executor.submit(self._get_single_head_fea, file)
                tasks.append(f)
        for _ in as_completed(tasks):
            # wait all thread tasks complete and then do sth
            # but i dont need future object's result
            pass
        # is there any better way to determin if the list of futures's status all done
        # without using `for ... else ...` such unelegent way?
        else:
            df = pd.DataFrame(self.head_fea_val, columns=self.head_fea)
            self.to_db(df, config.tbl_exp1_head_fea)
            logger.info(f'[feature extraction] head_hea has been stored!')

    def _extract_face_fea(self, file):
        """
        Input: data, the feature_2d in face, a dataframe with columns
        """
        fea_item = []
        ID = file.split('/')[-1][:3]; fea_item.append(ID)
        data = pd.read_csv(file, header=0)
        data.columns = [item.strip() for item in data.columns.values]

        # eye's fea
        left_eye_h_dist = data['x39'] - data['x36']
        fea_item += self.sf.gen_fea(left_eye_h_dist.values)
        right_eye_h_dist = data['x45'] - data['x42']
        fea_item += self.sf.gen_fea(right_eye_h_dist.values)
        
        left_eye_v_dist = data['y37'] - data['y41']
        right_eye_v_dist = data['y43'] - data['y47']
        fea_item += self.sf.gen_fea(left_eye_v_dist.values)
        fea_item += self.sf.gen_fea(right_eye_v_dist.values)

        # mouth fea 
        mouth_v_dist = data['y51'] - data['y57']
        mouth_h_dist = ((data['x54'] - data['x48']) \
                        + (data['x64'] - data['x59'])) / 2
        fea_item += self.sf.gen_fea(mouth_v_dist.values)
        fea_item += self.sf.gen_fea(mouth_h_dist.values)
                
        # eyebrow fea 
        eb_h_dist = ((data['x21'] - data['x22']) \
                        + (data['x26'] - data['x17'])) / 2
        eb_v_dist = ((data['y30'] - data['y25']) \
                        + (data['y30'] - data['y19'])) / 2
        fea_item += self.sf.gen_fea(eb_h_dist.values)
        fea_item += self.sf.gen_fea(eb_v_dist.values)
        self.face_fea_val.append(fea_item)
        logger.info(f'[feature extraction]: extract {ID} face featrue in exp1!')

    def gen_face_fea(self):
        folds = gen_file_path_by_fea('face_2d')
        with ThreadPoolExecutor() as executor:
            tasks = []
            for file in folds:
                f = executor.submit(self._extract_face_fea, file)
                tasks.append(f)
        for _ in as_completed(tasks):
            pass
        else:
            df = pd.DataFrame(self.face_fea_val, columns=self.face_fea)
            self.to_db(df, config.tbl_exp1_face_fea)
            logger.info(f'[feature extraction] face_hea has been stored!')

    def to_db(self, data_frame, table):
        sql_handler = SqlHandler()
        sql_handler.df_to_db(data_frame, table)


