"""
Extract aduio Low-Level Descriptors via OpenSMILE.
"""
import config
import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from common.log_handler import get_logger
from common.sql_handler import SqlHandler
from global_values import *
logger = get_logger()

# feature_type = 'egemaps'
# feature_type = 'mfcc'

def extract_audio(sample, prefix, opensmile_options, outputoption, feature_type):
    """Dispatch extraction tasks
    sample: phq-id like 310
    prefix: phq file prefix like 310_
    feature_type: mfcc or egemaps
    """
    infilename = f"{config.sample_dir}/{prefix}P/{prefix}{SUFFIX['wav']}"
    outfilename = f'{sample}_{feature_type}.csv'
    opensmile_call = config.opensmile_exe + ' ' + opensmile_options + ' -inputfile ' + infilename + ' ' + outputoption + ' ' + outfilename + ' -instname ' + str(sample) + ' -output ?'
    os.system(opensmile_call)
    if os.path.exists(outfilename): df = pd.read_csv(outfilename, sep=';')
    else:
        return sample, feature_type
    db_handler = SqlHandler()
    if feature_type == 'mfcc':
        db_handler.df_to_db(df, config.tbl_mfcc, if_exists='append')
    elif feature_type == 'egemaps':
        db_handler.df_to_db(df, config.tbl_egemaps, if_exists='append')
    os.remove(outfilename)
    return sample, feature_type
    

def get_audio_llds(feature_type):
    if feature_type == 'mfcc': 
        conf_smileconf = config.opensmile_config_path + '/MFCC12_0_D_A.conf'
        opensmile_options = '-configfile ' + conf_smileconf + ' -appendcsv 0 -timestampcsv 1 -headercsv 1'
        outputoption = '-csvoutput'
    elif feature_type == 'egemaps':
        conf_smileconf = config.opensmile_config_path + '/gemaps/eGeMAPSv01a.conf'
        opensmile_options = '-configfile ' + conf_smileconf + ' -appendcsvlld 0 -timestampcsvlld 1 -headercsvlld 1' 
        outputoption = '-lldcsvoutput' 
    else:
        logger.info('Error: Feature Type' + feature_type)
    with ThreadPoolExecutor(max_workers=20) as executor:
        tasks = []
        for sample, prefix in zip(IDS, PREFIX):
            tasks.append(executor.submit(extract_audio(sample, prefix, opensmile_options, 
                                       outputoption, feature_type)))
        for future in as_completed(tasks):
            try:
                res_sample, res_type = future.result()
                logger.info(f'[Feature Extration: Auido LLDs] {res_sample} {res_type} ...')
            except:
                continue
        
            
        
