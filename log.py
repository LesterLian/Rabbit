# -*- coding: utf-8 -*-
# @Time    : 1/25/18 6:26 PM
# @Author  : Lester
from datetime import datetime


class Log:
    def __init__(self, path):
        self.path_to_log = path or 'log'
        self.file = open(self.path_to_log, 'a')

    def log(self, message):
        timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())
        text = timestamp + '    ' + message
        print(text)
        self.file.write(text + '\n')

    def close(self):
        self.file.close()

    def clear(self):
        self.file.close()
        open(self.path_to_log, 'w').close()
        self.file = open(self.path_to_log, 'a')
