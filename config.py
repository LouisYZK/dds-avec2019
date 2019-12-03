import configparser
import ast
import common.log_handler as log_handler
import global_values

conf_file = global_values.BASE_DIR + 'config/config.ini.model'

config = configparser.ConfigParser()


trainable = None
data_dir = None

logger = None


def init():
    global trainable
    global data_dir
    global logger
    logger = log_handler.get_logger()

    config.read(conf_file)
    logger.debug(config)
    data_dir = config.get('data', 'data_dir')

    trainable = ast.literal_eval(config.get('training', 'trainable'))

    logger.info('Init!..')


if __name__ == '__main__':
    init()