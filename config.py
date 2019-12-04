import configparser
import ast
import common.log_handler as log_handler
import global_values

conf_file = global_values.BASE_DIR + 'config/config.ini.model'

config = configparser.ConfigParser()


trainable = None
data_dir = None

logger = None

# table's name here
feature_exp01 = None

# database info here
db_path = None
tbl_training_set = None
tbl_develop_set = None
tbl_test_set = None


def init():
    global trainable
    global data_dir
    global logger
    global feature_exp01
    global db_path, tbl_develop_set, tbl_training_set, tbl_test_set
    logger = log_handler.get_logger()

    config.read(conf_file)
    logger.debug(config)
    data_dir = config.get('data', 'data_dir')

    trainable = ast.literal_eval(config.get('training', 'trainable'))

    feature_exp01 = config.get('feature_table', 'tbl_exp01')
    db_path = config.get('database', 'db_path')
    tbl_training_set = config.get('database', 'tbl_training_set')
    tbl_develop_set = config.get('database', 'tbl_develop_set')
    tbl_test_set = config.get('database', 'tbl_test_set')

    logger.info('Init!..')


if __name__ == '__main__':
    init()