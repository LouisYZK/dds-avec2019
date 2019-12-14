"""
Use the feature originally in COVAREP and FORMANT
Extract some statistical features of them;

Audio feature with statistical feature are 547.

"""
import itertools
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from common.sql_handler import SqlHandler
from common.stats_features import StatsFea
from common.log_handler import get_logger
from global_values import *
import config

logger = get_logger()
stats_fea = StatsFea()

def gen_sigle_fea(fold):
    fea_item = list()
    fea_item.append(fold[:-1])
    path = f"{config.data_dir}avec/{fold}P/{fold}{SUFFIX['covarep']}"
    covarep =  pd.read_csv(path, header=None)
    covarep.columns = COVAREP_COLUMNS

    path = f"{config.data_dir}avec/{fold}P/{fold}{SUFFIX['formant']}"
    formant = pd.read_csv(path, header=None)
    formant.columns = FORMANT_COLUMNS
    
    covarep = covarep[covarep['VUV'] == 1]
    for fea in COVAREP_COLUMNS:
        if fea is 'VUV':
            continue
        else:
            fea_item += stats_fea.gen_fea(covarep[fea].values)

    for fea in FORMANT_COLUMNS:
        fea_item += stats_fea.gen_fea(formant[fea].values)
    logger.info(f'{fold} has been extrated audio feature in exp2!..')
    return fea_item

def gen_fea():
    sql_handler = SqlHandler()

    audio_value = list()
    with ThreadPoolExecutor(max_workers=30) as executor:
        task = [executor.submit(gen_sigle_fea, fold) for fold in PREFIX]
        for future in as_completed(task):
            try:
                fea_item = future.result()
                audio_value.append(fea_item)
            except:
                continue
                

    COVAREP_COLUMNS.remove('VUV')
    audio_fea = list()
    audio_fea.append('ID')
    COVAREP_COLUMNS.extend(FORMANT_COLUMNS)
    for a_fea, s_fea in itertools.product(COVAREP_COLUMNS, stats_fea.columns):
        audio_fea.append(a_fea + '_' + s_fea)
        
    assert len(audio_value[0]) == len(audio_fea)

    audio_df = pd.DataFrame(audio_value, columns=audio_fea)

    sql_handler.execute(f'drop table if exists {config.tbl_exp2_audio_fea};')
    sql_handler.df_to_db(audio_df, config.tbl_exp2_audio_fea)
    logger.info('audio feature exp2 has been stored!')
                

                