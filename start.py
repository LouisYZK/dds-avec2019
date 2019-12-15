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
parser.add_argument('--model', help='choose which predictor to train')

args = parser.parse_args()

if args.mode == 'extract':
    fea_ext = extract.FeatureExtration(model=args.feature)
    fea_ext.gen_fea()

elif args.mode == 'train':
    fea = args.feature
    model = args.model
    logger.info(f'You are training using model {model} via feature {fea}')
    training = Train(model_name=model, feature_name=fea)
    training.run()
    
else:
    logger.info('training model not finished yet!')