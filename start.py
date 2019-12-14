import sys
import config
config.init()
from global_values import *
import librosa
from core.feature_exraction.data_to_db import data_set
import common.log_handler as log_handler
logger = log_handler.get_logger()
from core.feature_exraction import extract

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--mode', help='feature extraction or training')
parser.add_argument('--model', help='choose which model')

args = parser.parse_args()

if args.mode == 'feature':
    fea_ext = extract.FeatureExtration(model=args.model)
    fea_ext.gen_fea()
else:
    logger.info('training model not finished yet!')