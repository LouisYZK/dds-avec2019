"""
Video LLDs are the Pose, Gaze postion and FAUs, 
which can be extracted via OpenSMILE.
But the work has been done in AVEC 2017's baseline.
"""
import config
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from common.log_handler import get_logger
from common.sql_handler import SqlHandler
from global_values import *
logger = get_logger()

def gather_video_llds(sample_id):
    """feature_type: gaze, pose or au
    """
    dfs = []
    for feature_type in ['pose', 'gaze', 'au']:
        try:
            file_dir = f'{config.sample_dir}/{sample_id}_P/{sample_id}_{SUFFIX[feature_type]}'
            dfs.append(pd.read_csv(file_dir))
        except:
            return
    df = pd.concat(dfs, axis=1)
    sql_handler = SqlHandler(config.db_type)
    sql_handler.df_to_db(df, config.tbl_pose_gaze_faus, if_exists='append')
    sql_handler.disconnect()
    logger.info(f'[Feature Extraction Video LLDs] {sample_id}')
    


def get_video_llds():
    with ThreadPoolExecutor(max_workers=20) as executor:
        tasks = []
        for sample in IDS:
            tasks.append(executor.submit(gather_video_llds(sample)))