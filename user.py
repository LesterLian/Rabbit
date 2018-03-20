# -*- coding: utf-8 -*-
# @Time    : 1/21/18 11:04 AM
# @Author  : Lester
import threading

L = threading.Lock()  # 引入锁


class User:
    def __init__(self):
        self.data = dict()
        # id phone pwd isTop

    def update(self, new_data):
        for key, val in new_data.items():
            self.data[key] = val

    def get(self, field):
        if self.has(field):
            return self.data[field]
        else:
            return None

    def has(self, other_key):
        for key, val in self.data.items():
            if key == other_key:
                return True
        return False
