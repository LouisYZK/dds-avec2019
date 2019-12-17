"""
generate file paths on giving feature;

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
"""
import config
from global_values import *

def gen_file_path_by_fea(fea_name):
    paths = list()
    for fold in PREFIX:
        path = f"{config.data_dir}avec/{fold}P/{fold}{SUFFIX[fea_name]}"
        paths.append(path)

    return paths


if __name__ == '__main__':
    print(gen_file_path_by_fea('covarep'))