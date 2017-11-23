# encoding=utf-8
import logging.handlers
import os

from singleton import Singleton

LOG_LEVEL_MAP = {
    'CRITICAL' : logging.CRITICAL,
    'FATAL' : logging.FATAL,
    'ERROR' : logging.ERROR,
    'WARNING' : logging.WARNING,
    'WARN' : logging.WARN,
    'INFO' : logging.INFO,
    'DEBUG' : logging.DEBUG,
    'NOTSET' : logging.NOTSET
}

basic_logger_names = ('face', 'mysql')

class PBSLogger:

    __metaclass__ = Singleton

    def __init__(self):
        self.__log_file = 'ff.log'
        self.__log_level = LOG_LEVEL_MAP['DEBUG']
        self.__log_backup_when = 'D'
        self.__log_backup_interval = 1
        self.__log_backup_count = 7

        self.__log_formater = logging.Formatter("[%(levelname)-5s] %(asctime)s : (%(name)s) %(message)s")

        log_file = self.__log_file
        self.__handler = logging.handlers.TimedRotatingFileHandler(log_file, self.__log_backup_when, self.__log_backup_interval, self.__log_backup_count)
        self.__handler.suffix = "%Y-%m-%d.log"
        self.__handler.setFormatter(self.__log_formater)
        log_folder = os.path.dirname(os.path.abspath(self.__log_file))
        try:
            os.stat(log_folder)
        except:
            os.mkdir(log_folder)
        logging.basicConfig(level=self.__log_level, format="[%(levelname)-5s] %(asctime)s : (%(name)s) %(message)s")

        for name in basic_logger_names:
            logger = logging.getLogger(name)
            if not logger.handlers:
                logger.addHandler(self.__handler)

    @staticmethod
    def getLogger(name='pbs'):
        helper = PBSLogger()
        logger = logging.getLogger(name)
        logger.setLevel(helper.__log_level)
        if not logger.handlers:
            logger.addHandler(helper.__handler)
        return logger

logger = PBSLogger().getLogger('face')

if __name__ == '__main__':
    logger.error("just for error test")