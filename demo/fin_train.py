import itertools
from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from scipy import interp
from sklearn.metrics import roc_auc_score
import numpy as np
import pandas as pd

from loguru import logger
import config 
from model_define import FaceStatsDataset

logger.add('result.log')
"""
'frame', 'face_id', 'timestamp', 'confidence','success',
gaze_0_(x,y,z), gaze_1_(x,y,z), gaze_angle_x, gaze_angle_y,
eye_lmk_(x,y)_(0,55), ege_lmk_(X,Y,Z)_(0,55)
pose_(Tx, Ty, Tz), pose_(Rx, Ry, Rz)
x_(0, 67), y(0,67), (X,Y,Z)_(0,67)
p_(rx, ry, rz), p(tx, ty), p_(0, 33)
AU
"""
feature = {}
feature['gaze_stats'] = [f'gaze_{i}_{j}' for i, j in itertools.product(range(2), 'xyz')]
# feature['pose_stats'] = [f'{i}_{j}' for i, j in itertools.product('xy', range(68))]
# feature['']

for feature_name, feature_cols in feature.items():
    logger.info(f'{feature_name} start training...')
    ds = FaceStatsDataset(feature_columns=feature_cols)
    X, y = ds[:]
    y = np.vstack(y)
    for size, model in zip([.3, .4, .5], ['logistic', 'svm']):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=size, random_state=0)
        if model == 'svm':
            clf = svm.SVC(kernel='linear', probability=True,
                          random_state=0)
            y_score = clf.fit(X_train, y_train).decision_function(X_test)
        elif model == 'logistic':
            clf = LogisticRegression().fit(X_train, y_train)
            y_score = clf.predict_proba(X_test)[:,1]
        fpr, tpr, _ = roc_curve(y_test, y_score)
        auc_score = auc(fpr, tpr)
        logger.info(f'{feature_name} with Test Size {size}, Model {model} get AUC: {auc_score}.')
