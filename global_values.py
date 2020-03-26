import os
import config
BASE_DIR = '/home/yzk/dds-avec2019/'

TRAIN_SET_NAME = 'train_split_Depression_AVEC2017.csv'
DEL_SET_NAME = 'dev_split_Depression_AVEC2017.csv'

# COVAREP's clomuns
COVAREP_COLUMNS = ['F0', 'VUV', 'NAQ', 'QOQ', 'H1H2', 'HRF', 'PSP', 'MDQ', 'peakSlope',
'Rd', 'Rd_conf']
for i in range(25): COVAREP_COLUMNS.append('MCEP_' + str(i))
for i in range(25): COVAREP_COLUMNS.append('HMPDM_' + str(i))
for i in range(13): COVAREP_COLUMNS.append('HMPDD_' + str(i))

"""
F0 - Fundamental Frequnency; 原始的声带振动频率，决定了声音的初始音高；一般是在语谱图中最低的共振峰；
VUV - 0,1 表示声音的有无
NAQ - Normalized amplitude quotient
QOQ - quasi-open quotient
-------------以下是频域
H1H2 - the difference in amplitude of the first two harmonics of the differentiated glottal source spectrum 
HRF - Harmonic richness factor
PSP - Parabolic spectral parameter
MDQ - The Maxima Dispersion Quotient (MDQ) quantifies how impulse-like the 
       glottal excitation is through wavelet analysis of the Linear Prediction(LP) residual
peakSlope - A parameter which is essentially a correlate of spectral tilt, derived
            following wavelet analysis. This parameter is effective at discriminating
            lax-tense phonation types
---------- 主要针对LF model
Rd -  estimation of the LF glottal model using Mean Squared Phase (MSP)
Rd_conf -  a confidence value between 0 (lowest confidence) to 1 (best confidence). 
            This last value describes how well the glottal model fits the signal.
---------- HM 谐波模型 主要研究谐波的相位表示
HM PDD - Phase Distortion 导数
HM PDM - Phase Distortion Mean
"""

PREFIX = [folder[:-1] for folder in os.listdir(config.data_dir + '/avec') \
                                  if folder.endswith('P')]
IDS = [item[:3] for item in PREFIX]

SUFFIX = {
    'wav': 'AUDIO.wav',
    'face_3d': 'CLNF_features3D.txt',
    'face_2d': 'CLNF_features.txt',
    'gaze': 'CLNF_gaze.txt',
    'pose': 'CLNF_pose.txt',
    'formant': 'FORMANT.csv',
    'text': 'TRANSCRIPT.csv',
    'au': 'CLNF_AUs.txt',
    'hog': 'CLNF_hog.bin',
    'covarep': 'COVAREP.csv'
}

# formant.csv columns
FORMANT_COLUMNS = ['formant_0', 'formant_1', 'formant_2', 'formant_3', 'formant_4']
# column name of video
POSE_COLUMNS = ['Tx', 'Ty',	'Tz', 'Rx', 'Ry', 'Rz']
EXP1_FACE_COLUMNS = ['right_eye_h', 'left_eye_h', 'left_eye_v', 'right_eye_v',
                'mouth_v', 'mouth_h', 'eyebrow_h', 'eyebrow_v']

# feature's name 
FEATURE_EXP_1 = 'exp1'
FEATURE_EXP_2 = 'exp2'
FEATURE_BL = 'baseline'

# model's name
MODEL_RF = 'rf'


AUDIO_TABLE = set([
    config.tbl_exp2_audio_fea
])

VIDEO_TABLE = set([
    config.tbl_exp1_face_fea,
    config.tbl_exp1_head_fea
])

TEXT_TABLE = set([])
