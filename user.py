# -*- coding: utf-8 -*-
# @Time    : 1/21/18 11:04 AM
# @Author  : Lester
import threading

L = threading.Lock()  # 引入锁


class User:
    def __init__(self):
        self.data = dict()

    def update(self, new_data):
        for key, val in new_data.items():
            self.data[key] = val

    def find(self, field):
        return self.data[field]
