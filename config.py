import configparser
import ast
import common.log_handler as log_handler

BASE_DIR = '/home/yzk/dds-avec2019/'

conf_file = BASE_DIR + 'config/config.ini.model'
config = configparser.ConfigParser()


trainable = None
data_dir = None
sample_dir = None

logger = None

# table's name here
feature_exp01 = None

# database info here
db_path = None
tbl_training_set = None
tbl_develop_set = None
tbl_test_set = None
tbl_exp2_audio_fea = None
tbl_exp1_head_fea = None
tbl_exp1_face_fea = None
tbl_mfcc = None
tbl_egemaps = None
tbl_boaw_mfcc = None
tbl_boaw_egemaps = None
tbl_audio_densenet = None
tbl_audio_vgg = None
tbl_pose_gaze_faus = None
tbl_bovw_pose_gaze_faus = None
tbl_cnn_restnet = None
tbl_cnn_vgg = None

# mysql
mysql_username = None
mysql_host = None
mysql_port = None
mysql_password = None
mysql_db = None

# opensmile
opensmile_exe = None
opensmile_config_path = None

#oepnxbow
jar_path = None

def init():
    global trainable
    global data_dir, sample_dir
    global logger
    global feature_exp01
    global db_path, tbl_develop_set, tbl_training_set, tbl_test_set, tbl_exp2_audio_fea, tbl_mfcc, tbl_egemaps, tbl_boaw_mfcc, tbl_boaw_egemaps, tbl_audio_densenet, tbl_audio_vgg, tbl_pose_gaze_faus, tbl_bovw_pose_gaze_faus, tbl_cnn_restnet, tbl_cnn_vgg
    global mysql_username, mysql_host, mysql_port, mysql_password , mysql_db
    global tbl_exp1_face_fea, tbl_exp1_head_fea
    global opensmile_config_path, opensmile_exe
    global jar_path
    logger = log_handler.get_logger()
    
    config.read(conf_file)
    data_dir = config.get('data', 'data_dir')
    sample_dir = config.get('data', 'sample_dir')

    trainable = ast.literal_eval(config.get('training', 'trainable'))

    feature_exp01 = config.get('feature_table', 'tbl_exp01')
    db_path = config.get('database', 'db_path')
    tbl_training_set = config.get('database', 'tbl_training_set')
    tbl_develop_set = config.get('database', 'tbl_develop_set')
    tbl_test_set = config.get('database', 'tbl_test_set')
    tbl_exp2_audio_fea = config.get('database', 'tbl_exp2_audio_fea')
    tbl_exp1_head_fea = config.get('database', 'tbl_exp1_head_fea')
    tbl_exp1_face_fea = config.get('database', 'tbl_exp1_face_fea')
    tbl_mfcc = config.get('database', 'tbl_mfcc')
    tbl_egemaps = config.get('database', 'tbl_egemaps')
    tbl_boaw_mfcc = config.get('database', 'tbl_boaw_mfcc')
    tbl_boaw_egemaps = config.get('database', 'tbl_boaw_egemaps')
    tbl_audio_densenet = config.get('database', 'tbl_audio_densenet')
    tbl_audio_vgg = config.get('database', 'tbl_audio_vgg')
    tbl_pose_gaze_faus = config.get('database', 'tbl_pose_gaze_faus')
    tbl_bovw_pose_gaze_faus = config.get('database', 'tbl_bovw_pose_gaze_faus')
    tbl_cnn_restnet = config.get('database', 'tbl_cnn_resnet')
    tbl_cnn_vgg = config.get('database', 'tbl_cnn_vgg')

    mysql_username = config.get('mysql', 'username')
    mysql_host = config.get('mysql', 'host')
    mysql_port = config.get('mysql', 'port')
    mysql_password = config.get('mysql', 'password')
    mysql_db = config.get('mysql', 'db')

    opensmile_exe = config.get('opensmile', 'exe_opensmile')
    opensmile_config_path = config.get('opensmile', 'path_config')

    jar_path = config.get('openxbow', 'jar_path')

    logger.info('Init!..')


if __name__ == '__main__':
    init()