#coding:utf-8

import logging
from logging import handlers
import os


class Logger(object):

    def __init__(self, backup_count, level):
        self.log_name = 'tutorial.log'
        self.log_dir = os.path.join('..', 'log')
        self.log_path = os.path.join(self.log_dir, self.log_name)
        self.__create_log_directory()
        self.__init_logger(backup_count, level)

    # private attribute
    def __create_log_directory(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def __init_logger(self, backup_count, level):
        self.logger = logging.getLogger()
        handler = logging.handlers.TimedRotatingFileHandler(
            self.log_path,
            when='D',
            interval=1,
            backupCount=backup_count)
        formatter = logging.Formatter(
            '[%(asctime)s] '
            '[%(levelname)s] '
            '[%(thread)d] '
            '[%(module)s:%(lineno)d] '
            '%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(level)


class Error(Exception):
    pass