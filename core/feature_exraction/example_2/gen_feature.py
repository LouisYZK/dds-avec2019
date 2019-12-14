"""
Use the feature originally in COVAREP and FORMANT
Extract some statistical features of them;
"""
import itertools
import pandas as pd
from common.sql_handler import SqlHandler
from common.stats_features import StatsFea
from common.log_handler import get_logger
from global_values import *
import config

logger = get_logger()

def gen_fea():
    sql_handler = SqlHandler()
    stats_fea = StatsFea()

    audio_value = list()
    for fold in PREFIX:
        fea_item = list()
        fea_item.append(fold[:-1])
        try:
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

            audio_value.append(fea_item)
            logger.info(f'{fold} extract audio feature in exp2 finished!')
        except:
            logger.debug(f'{fold} file exist error, skip...')
            continue

    COVAREP_COLUMNS.remove('VUV')
    audio_fea = list()
    audio_fea.append('ID')
    fea = COVAREP_COLUMNS.extend(FORMANT_COLUMNS)
    for a_fea, s_fea in itertools.product(fea, stats_fea.columns):
        audio_fea.append(a_fea + '_' + s_fea)
        
    logger.info('audio feature:', audio_fea)
    
    assert len(audio_value[0]) == len(audio_fea)

    audio_df = pd.DataFrame(audio_value, columns=audio_fea)

    sql_handler.execute(f'drop table {config.tbl_exp2_audio_fea}')
    sql_handler.df_to_db(audio_df, config.tbl_exp2_audio_fea)
    logger.info('audio feature exp2 has been stored!')
                

                