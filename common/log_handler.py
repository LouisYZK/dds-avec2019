import os
import logging.handlers
import logging.config
# LOG_HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_logger = None
def get_logger():
    global _logger
    if _logger:
        return _logger
    logging.config.fileConfig("config/logger.conf")
    _logger = logging.getLogger("root")
    return _logger
