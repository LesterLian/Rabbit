# -*- coding: UTF-8 -*-
# @Time    : 1/25/18 6:26 PM
# @Author  : Lester
from datetime import datetime
from post.post import Post


class Log:
    def __init__(self, path):
        self.path_to_log = path or 'log'
        self.file = open(self.path_to_log, 'w', encoding='utf8')

    def log(self, message):
        timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())
        text = timestamp + '    '

        if message is None:
            text += 'POST has no response.'
        elif message.__class__ is Post:
            text += message.response_json['message']
        elif message.__class__ is str:
            text += message
        print(text)
        self.file.write(text + '\n')

    def close(self):
        self.file.close()

    def clear(self):
        self.file.close()
        open(self.path_to_log, 'w', encoding='utf8').close()
        self.file = open(self.path_to_log, 'a', encoding='utf8')
