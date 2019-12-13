import config
import os
BASE_DIR = '/home/yzk/dds-avec2019/'

TRAIN_SET_NAME = 'train_split_Depression_AVEC2017.csv'
DEL_SET_NAME = 'dev_split_Depression_AVEC2017.csv'

# COVAREP's clomuns
COVAREP_COLUMN = ['F0', 'VUV', 'NAQ', 'QOQ', 'H1H2', 'HRF', 'PSP', 'MDQ', 'peakSlope',
'Rd', 'Rd_conf']
for i in range(25): COVAREP_COLUMN.append('MCEP_' + str(i))
for i in range(25): COVAREP_COLUMN.append('HMPDM_' + str(i))
for i in range(13): COVAREP_COLUMN.append('HMPDD_' + str(i))

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