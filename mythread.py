# -*- coding: utf-8 -*-
# @Time    : 3/19/18 11:27 PM
# @Author  : Lester

from PyQt5.QtCore import QThread, pyqtSignal
from director import Director
from user import User
from time import sleep


class MyThread(QThread):
    update_signal = pyqtSignal(int, User)
    finished_signal = pyqtSignal()

    def __init__(self):
        super(QThread, self).__init__()
        self.user_list = list()

    def __del__(self):
        self.wait()

    def pass_user_list(self, users):
        self.user_list = users

    def run(self):
        print('run')
        for row in range(len(self.user_list)):
            print('printing', str(row))
            user = self.user_list[row]
            # 跳过
            if user.get('completed') == '完成' if user.has('completed') else False:
                print('跳过')
                continue
            # TODO afs_token
            # self.browser = Browser()
            # user.update({'afs_token': self.browser.afs_token})
            user.update({'afs_token': ''})
            director = Director(user)
            # 运行
            director.run()
            # 回显
            if not director.tag:
                user.update({'completed': '失败'})
                print('Director failed')
            else:
                completed = '完成' if director.wrong_info == [] else '未完成打扫' if director.wrong_info == ['打扫'] else '失败'
                user.update({'completed': completed})
            # 命令行回显
            if not director.wrong_info:
                print(user.get('phone') + ": " + "成功" +
                      " 兔子数：" + user.get('chickenCount'))
            else:
                print(user.get('phone') + ": " + "失败" + str(director.wrong_info) +
                      " 兔子数：" + str(user.get('chickenCount')) if user.has('chickenCount') else '')
            # TODO delete test
            # user.update({'completed': 'test', 'chickenCount': str(row), 'eggCount': str(row+1)})
            # sleep(1)

            self.update_signal.emit(row, user)
        self.finished_signal.emit()
