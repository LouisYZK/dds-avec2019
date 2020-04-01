import sys
import config
config.init()
from global_values import *
import librosa
from core.feature_exraction.data_to_db import data_set
import common.log_handler as log_handler
logger = log_handler.get_logger()
from core.feature_exraction import extract
from core.predictor.training import Train
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--mode', help='feature extraction or training')
parser.add_argument('--feature', help='choose which feature to extract or train')
parser.add_argument('--feature_tables', help='choose the feature to train using tables name',
                    type=list)
parser.add_argument('--model', help='choose which predictor to train')
parser.add_argument('--gender', help='wether consider gender or not')
parser.add_argument('--db', help='choose which database version you use, sqlite or mysql')

args = parser.parse_args()

if args.db is not None:
    config.db_type = args.db

if args.mode == 'extract':
    # fea_ext = extract.FeatureExtration(model=args.feature)
    fea_ext = extract.FeatureExtration(feature_name=args.feature)
    fea_ext.gen_fea()

elif args.mode == 'train':
    if args.feature is not None:
        fea = args.feature
        model = args.model
        logger.info(f'You are training using model {model} via feature {fea}')
        training = Train(model_name=model, feature_name=fea)
        training.start()
        if args.gender == 'y':
            logger.info(f'You are training using model {model} via feature {fea} and consider gender!')
            Train(model_name=model, feature_name=fea, gender=True).start()
    else:
        fea_tables = args.feature_tables
        model = args.model
        logger.info(f'[Training] You are using model {model} via feature table {fea_tables}')
        training = Train()
elif args.mode == 'database':
    from common.sql_handler import SqlHandler
    sql_handler = SqlHandler()
    sql_handler.print_tables()  
else:
    logger.info('training model not finished yet!')