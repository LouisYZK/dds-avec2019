import sys
import config
import librosa
from core.feature_exraction.data_to_db import data_set
import common.log_handler as log_handler
config.init()


data_set()
