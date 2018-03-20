# -*- coding: utf-8 -*-
# @Time    : 3/19/18 11:27 PM
# @Author  : Lester

from PyQt5.QtCore import QThread

class MyThread(QThread):
    def __init__(self, func):
        super(QThread, self).__init__()
        self.function = func

    def __del__(self):
        self.wait()

    def run(self):
        self.function()
