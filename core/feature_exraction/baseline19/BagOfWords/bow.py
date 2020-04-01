"""
Using OpenXBOW to extract Bag of Words feature from LLDs
https://github.com/openXBOW/openXBOW
IO handler: 
db --> mfcc.csv -->(OpenXBow) --> bow.csv --> db
"""
import os
import traceback
import pandas as pd
import config
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from common.sql_handler import SqlHandler
from common.log_handler import get_logger
logger = get_logger()

def worker(sample_id):
    sql = f"select * from {config.tbl_mfcc} where substr(name, 2, 3) ='{sample_id}' "
    print('Start......', sample_id)
    sql_handler = SqlHandler()
    res = sql_handler.get_df(sql=sql)
    sql_handler.disconnect()
    return res

def gen_bow(modal, llds,
            window_size=4,
            hop_size=0.5,
            size=100,
            a=1,
            attributes='nt1[39]',
            log=None,
            ):
    """generate bow (boaw or bovw) features from llds:
    Args:
        modal:                     video, audio or text
        llds:                      lld name , example: mfcc
        window_szie and hop_szie:  '-t' param in OpenXBOW
        size:                      codebook length, can be seen as cluster numbers
                                   and '-size' param in OpenXBOW
        a:                         the number of nearest nodes in clustering, 1 in defalt
        attributes:                split the feature into subsets to train cluster model
                                   it is the '--attributes' param on OpenXBOW
        log:                       the histgram representation of BoW vector
    """

    if modal == 'audio':
        if llds == 'mfcc':
            table_name = config.tbl_mfcc
            outpot_table = config.tbl_boaw_mfcc
        elif llds == 'egemaps':
            table_name = config.tbl_egemaps
            output_table = config.tbl_boaw_egemaps
    elif modal == 'video':
        if llds == 'pose_gaze_faus':
            table_name = config.tbl_pose_gaze_faus
            output_table = config.tbl_bovw_pose_gaze_faus
    # prepare llds data
    input_file = table_name + '_llds.csv'
    if not os.path.exists(input_file):
        sql_handler = SqlHandler()
        names = sql_handler.query("select distinct substr(name, 2,3) from %s" % table_name)
        # sql_handler.disconnect()
        # with ThreadPoolExecutor(max_workers=30) as executor:
        #     sql_handler = SqlHandler()
        #     tasks = [executor.submit(worker, name[0]) for name in names]
        # dfs = []
        # for future in as_completed(tasks):
        #     print(future.result().head())
        #     df = future.result().drop(['frameTime'], axis=1)
        #     dfs.append(df)
        dfs = []
        def name_process(x):
            return int(x['name'][1:4])
        for name in names:
            try:
                sql = f"select * from {table_name} where substr(name, 2, 3) ='{name[0]}' "
                df = sql_handler.get_df(sql=sql).drop(['frameTime'], axis=1)
                df['name'] = df.apply(name_process, axis=1)
                dfs.append(df)
            except Exception as e:
                traceback.print_exc()
                import sys
                sys.exit()
                continue
        mfcc_df = pd.concat(dfs, axis=0)  # stack by row
        mfcc_df.to_csv(input_file, header=None, sep=';')

    openxbow = 'java -jar ' + config.jar_path + ' -i ' + input_file
    output_file = table_name + '_bow.csv'
    if os.path.exists(output_file): os.system(f'rm {output_file}')
    openxbow += f' -o {output_file}'
    openxbow += f' -attributes {attributes}'
    openxbow += f' -t {window_size} {hop_size} '
    openxbow += f' -size {size}'
    if a is not None:
        openxbow += f' -a {a}'
    if log is not None:
        openxbow += f' -log {log}'

    logger.info(openxbow)
    try:
        logger.info("[OpXBOW Starting....]")
        print(openxbow)
        os.system(openxbow)
    except:
        logger.info('Failing OpenXBOW....')
        return
    if os.path.exists(output_file):
        sql_handler = SqlHadnler()
        df = pd.read_csv(output_file, sep=';')
        sql_handler.df_to_db(df, output_table, if_exists='replace')
        logger.info(f'Store OpenXBOW...{output_table}')