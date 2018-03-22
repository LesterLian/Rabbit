# -*- coding: utf-8 -*-
# @Time    : 1/30/2018 11:32 PM
# @Author  : Lester
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import QDateTime, QTimer
from gui_popup3 import Ui_Dialog
from ui import Ui_MainWindow
from user import User
from director import Director
from webkit import Browser
from mythread import MyThread
from time import sleep


class AppWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        # 主界面
        self.ui = Ui_MainWindow(self)

        # 读取用户文件
        self.user_list = []
        self.user_file = None

        # init user
        try:
            self.user_file = open('user', 'r')
            for line in self.user_file.readlines():
                temp = line.split()
                user = User()
                user.update({'phone': temp[0], 'pwd': temp[1], 'isTop': temp[2]})
                self.user_list.append(user)
                # self.ui.table.insertRow(self.ui.table.rowCount())
                # self.ui.table.setItem(self.ui.table.rowCount() - 1, 0, QTableWidgetItem(temp[0]))
                self.user_file.close()
        except FileNotFoundError:
            print('User File Not Found')
            self.user_file = open('user', 'w')
            self.user_file.close()

        self.init_table()

        # print('refresh')
        # self.refresh_table()
        # 弹窗
        self.child = Ui_Dialog()
        # 计时器
        self.timer = QTimer()
        # TODO 每天晚上帮下线收兔，再帮他们打扫
        self.daily_timer = QTimer()
        # TODO 周一下午要帮下线收兔
        self.weekly_timer = QTimer()
        # 每日清楚计时
        self.clear_timer = QTimer()
        # 网页
        self.browser = Browser()
        # 信号-槽
        # ximi edit
        # self.ui.popButton.clicked.connect(lambda: {self.child.exec_(), self.refresh_table()})
        self.ui.popButton.clicked.connect(lambda: self.child.exec_())
        # TODO delete
        # self.ui.runButton.clicked.connect(lambda: self.run_button(0))
        self.work = MyThread()
        self.work.update_signal.connect(lambda p1, p2: self.thread_callback(p1, p2))
        self.work.finished_signal.connect(lambda: self.ui.runButton.setDisabled(False))
        self.ui.runButton.clicked.connect(lambda: {
            self.work.pass_user_list(self.user_list),
            self.work.start(),
            self.ui.runButton.setDisabled(True),
            print('runButton returned')
        })
        self.ui.deleteButton.clicked.connect(lambda: self.delete_button())
        self.child.ButtonBox.accepted.connect(lambda: self.child_accept())
        # todo 检查timer逻辑
        self.timer.timeout.connect(lambda: self.timer_process_user(1))
        self.daily_timer.timeout.connect(lambda: {
            # 停止当前timer
            self.daily_timer.stop(),
            self.timer.stop(),
            self.timer_process_user(0),
            # timing至第二天0300
            self.clear_timer.start((115200 - QDateTime.currentDateTime() % 86400) * 1000)
        })
        # self.daily_timer.timeout.connect(self.daily_work())
        self.weekly_timer.timeout.connect(lambda: {
            # 停止当前timer
            self.weekly_timer.stop(),
            self.daily_timer.stop(),
            self.timer.stop(),
            self.timer_process_user(0),
            # timing至第二天0300
            self.clear_timer.start((115200 - QDateTime.currentDateTime() % 86400) * 1000)
        })
        self.clear_timer.timeout.connect(lambda: {
            # 每天0300
            # 重新开启daily, weekly timer
            self.timer_switch(),
            # 清空完成状态
            self.clear_completion()
        })
        self.ui.radioButton.toggled.connect(lambda: self.timer_switch())
        self.ui.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.table.setSelectionBehavior(QAbstractItemView.SelectRows)

    def thread_callback(self, row, user):
        self.ui.table.setItem(row, 1, QTableWidgetItem(user.get('completed')))
        self.ui.table.setItem(row, 2, QTableWidgetItem(user.get('chickenCount')))
        self.ui.table.setItem(row, 3, QTableWidgetItem(user.get('eggCount')))

    def init_table(self):
        for row in range(len(self.user_list)):
            self.add_table(row)  # init table

    # TODO deprecated
    # def update_table(self, row):
    #     user = self.user_list[row]
    #     # 跳过
    #     if user.get('completed') == '完成' if user.has('completed') else False:
    #         print('跳过')
    #         return
    #     # TODO afs_token
    #     # self.browser = Browser()
    #     # user.data['afs_token'] = self.browser.get_token()
    #     user.update({'afs_token': self.browser.afs_token})
    #     director = Director(user)
    #     # 运行
    #     director.run()
    #     # 回显
    #     if not director.tag:
    #         self.ui.table.setItem(row, 1, QTableWidgetItem('失败'))
    #         user.update({'completed': '失败'})
    #         print('Director failed')
    #     # print(director.user.data)
    #     # TODO Encapsulate
    #     completed = '完成' if director.wrong_info == [] else '未完成打扫' if director.wrong_info == ['打扫'] else '失败'
    #     self.ui.table.setItem(row, 1, QTableWidgetItem(completed))
    #     user.update({'completed': completed})
    #     self.ui.table.setItem(row, 2, QTableWidgetItem(
    #         user.get('chickenCount')
    #         if user.has('chickenCount') else ''))
    #     self.ui.table.setItem(row, 3, QTableWidgetItem(
    #         user.get('eggCount')
    #         if user.has('eggCount') else ''
    #     ))
    #     if not director.wrong_info:
    #         print(user.get('phone') + ": " + "成功" +
    #               " 兔子数：" + user.get('chickenCount'))
    #
    #     else:
    #         print(user.get('phone') + ": " + "失败" + str(director.wrong_info) +
    #               " 兔子数：" + str(user.get('chickenCount')) if user.has('chickenCount') else '')

    def add_table(self, row):
        self.ui.table.insertRow(row)
        self.ui.table.setItem(row, 0, QTableWidgetItem(self.user_list[row].data['phone']))
        self.ui.table.setItem(row, 4, QTableWidgetItem("是" if self.user_list[row].data['isTop'] == '0' else "否"))

    def delete_button(self):
        for row in sorted(set(index.row() for index in self.ui.table.selectedIndexes()), reverse=True):
            self.ui.table.removeRow(row)
            self.user_list.pop(row)
        self.refresh_user_file()

    def refresh_user_file(self):
        self.user_file = open('user', 'w')
        for user in self.user_list:
            self.user_file.write(
                user.get('phone') +
                ' ' + user.get('pwd') + ' ' + user.get('isTop') + '\n')
        self.user_file.close()

    def daily_work(self):
        self.ui.runButton.click()
        self.daily_timer.start(86400000)

    def timer_process_user(self, periodic):
        # periodic: 0: no timer, daily, weekly; 1: normal timer
        new_user_list = list()

        if periodic == 0:
            # 先下线 再上线
            for user in self.user_list:
                if user.get('isTop') == '0':
                    new_user_list.append(user)
        for user in self.user_list:
            if user.get('isTop') == '1':
                new_user_list.append(user)

        self.work.pass_user_list(new_user_list)
        self.work.start()

    def child_accept(self):
        flag = 1
        phone = self.child.LineEdit_account.text()
        pwd = self.child.LineEdit_password.text()

        if phone == '' or pwd == '':
            flag = 0

        for user in self.user_list:
            if user.get('phone') == phone:
                flag = 0
                break
        if self.child.checkBox_isTop.isChecked():
            is_top = '0'
        else:
            is_top = '1'
        if flag == 1:
            # self.ui.table.insertRow(self.ui.table.rowCount())
            # self.flash_table_passport()
            self.child.LineEdit_account.clear()
            self.child.LineEdit_password.clear()
            self.child.LineEdit_account.setFocus(0)

            # add to user_list
            user = User()
            user.update(({'phone': phone, 'pwd': pwd,
                          'isTop': is_top}))
            self.user_list.append(user)
            # add to table
            self.add_table(self.ui.table.rowCount())
            print('user list', self.user_list[-1].__class__, len(self.user_list))
            try:
                user_file = open('user', 'a+')
                user_file.write(phone + ' ' + pwd + ' ' + str(is_top) + '\n')
                user_file.close()
            except FileExistsError:
                print('file error')
            print('ok')
        else:
            print('重复passport')

    def timer_switch(self):
        daily = (55800 - QDateTime.currentDateTime().toTime_t() % 86400) * 1000
        weekly = (363600 - QDateTime.currentDateTime().toTime_t() % 604800) * 1000
        if daily < 0:
            self.ui.radioButton.setChecked(False)
            return
        if self.ui.radioButton.isChecked():
            self.timer_process_user(1)
            self.timer.start(1800000)
            self.daily_timer.start(daily)
            print('daily timer:', self.daily_timer.remainingTime())
            if weekly < 0:
                print("weekly not started")
            else:
                self.weekly_timer.start(weekly)
                print('weekly timer:', self.weekly_timer.remainingTime())
        else:
            self.timer.stop()
            self.daily_timer.stop()
            self.weekly_timer.stop()
            self.clear_timer.stop()

    def clear_completion(self):
        for row in range(len(self.user_list)):
            user = self.user_list[row]
            user.update({'completed': ""})
            self.ui.table.setItem(row, 1, QTableWidgetItem(""))


app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
