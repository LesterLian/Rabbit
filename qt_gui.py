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
        # self.weekly_timer = QTimer()
        # 网页
        self.browser = Browser()
        # 信号-槽
        # ximi edit
        # self.ui.popButton.clicked.connect(lambda: {self.child.exec_(), self.refresh_table()})
        self.ui.popButton.clicked.connect(lambda: self.child.exec_())
        self.ui.runButton.clicked.connect(lambda: self.run_button(0))
        self.ui.deleteButton.clicked.connect(lambda: self.delete_button())
        self.child.ButtonBox.accepted.connect(self.child_accept)
        # self.timer.timeout.connect(self.run_button(1))
        # todo timer逻辑
        self.daily_timer.timeout.connect(lambda: {self.run_button(0),
                                         self.daily_timer.start(86400000),
                                         print('daily timer:', self.daily_timer.remainingTime())})
        # self.timer.timeout.connect(lambda: self.ui.runButton.click())
        # todo timer逻辑
        # self.daily_timer.timeout.connect(self.ui.pushButton_2.click(),
        #                                  self.daily_timer.start(86400000),
        #                                  print('daily timer:', self.daily_timer.remainingTime()))
        # self.daily_timer.timeout.connect(self.daily_work())
        self.weekly_timer.timeout.connect(lambda: {self.run_button(0),
                                                   self.weekly_timer.start(604800000),
                                                   print('weekly timer:', self.weekly_timer.remainingTime())})
        self.ui.radioButton.toggled.connect(lambda: self.timer_switch())
        self.ui.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.table.setSelectionBehavior(QAbstractItemView.SelectRows)

    def init_table(self):
        for row in range(len(self.user_list)):
            self.add_table(row)  # init table

    def update_table(self, row):
        user = self.user_list[row]
        # 跳过
        if user.find('completed') == '完成' if user.has('completed') else False:
            print('跳过')
            return
        # TODO afs_token
        self.browser = Browser()
        # user.data['afs_token'] = self.browser.get_token()
        user.update({'afs_token': self.browser.afs_token})
        director = Director(user)
        # 运行
        director.run()
        # 回显
        if not director.tag:
            self.ui.table.setItem(row, 1, QTableWidgetItem('失败'))
            user.update({'completed': '失败'})
            print('Director failed')
        # print(director.user.data)
        # TODO Encapsulate
        completed = '完成' if director.wrong_info == [] else '未完成打扫' if director.wrong_info == ['打扫'] else '失败'
        self.ui.table.setItem(row, 1, QTableWidgetItem(completed))
        user.update({'completed': completed})
        self.ui.table.setItem(row, 2, QTableWidgetItem(
            user.find('chickenCount')
            if user.has('chickenCount') else ''))
        self.ui.table.setItem(row, 3, QTableWidgetItem(
            user.find('eggCount')
            if user.has('eggCount') else ''
        ))
        if not director.wrong_info:
            print(user.find('phone') + ": " + "成功" +
                  " 兔子数：" + user.find('chickenCount'))

        else:
            print(user.find('phone') + ": " + "失败" + str(director.wrong_info) +
                  " 兔子数：" + str(user.find('chickenCount')) if user.has('chickenCount') else '')
    def add_table(self, row):
        self.ui.table.insertRow(row)
        self.ui.table.setItem(row, 0, QTableWidgetItem(self.user_list[row].data['phone']))
        self.ui.table.setItem(row, 4, QTableWidgetItem("是" if self.user_list[row].data['isTop'] == '0' else "否"))

    def delete_button(self):
        for row in sorted(set(index.row() for index in self.ui.table.selectedIndexes()), reverse=True):
            self.ui.table.removeRow(row)
            self.user_list.pop(row)
        self.refresh_user_file()
        # TODO deprecated
        # row = self.ui.table.currentRow()
        #
        # self.ui.table.selectedItems()
        # self.ui.table.removeRow(row)
        # self.user_list.pop(row)
        # self.refresh_user_file()

    def refresh_user_file(self):
        self.user_file = open('user', 'w')
        for user in self.user_list:
            self.user_file.write(
                user.find('phone') +
                ' ' + user.find('pwd') + ' ' + user.find('isTop') + '\n')
        self.user_file.close()

    def daily_work(self):
        self.ui.runButton.click()
        self.daily_timer.start(86400000)

    # deprecated
    # def delete_button_old(self):
    #     indices = self.ui.table.selectedIndexes()
    #     rows = list()
    #     for index in indices:
    #         row = index.row()
    #         append = True
    #         for row_num in rows:
    #             if row_num == row:
    #                 append = False
    #         if append:
    #             rows.insert(0, index.row())
    #     for row in rows:
    #         self.ui.table.removeRow(row)
    #         self.passport_list.pop(row)
    #
    #     self.user_file = open('user', 'w')
    #     for passport in self.passport_list:
    #         self.user_file.write(passport['phone'] + ' ' + passport['pwd'] + '\n')
    #     self.user_file.close()

    def run_button(self, periodic):
        # periodic: 0: no timer, daily, weekly; 1: normal timer
        if periodic == 0:
            # 先下线 再上线
            for row in range(len(self.user_list)):
                if self.user_list[row].find('isTop') == '0':
                    self.update_table(row)
        for row in range(len(self.user_list)):
            if self.user_list[row].find('isTop') == '1':
                self.update_table(row)

    # deprecated
    # def run_button_old(self):
    #     self.user_file.close()
    #     i = 0
    #
    #     for passport in self.passport_list:
    #         # 跳过
    #         if self.ui.table.item(i, 1).text() == '完成' if self.ui.table.item(i, 1) else False:
    #             print('跳过')
    #             i += 1
    #             continue
    #         # 初始化
    #         user = User()
    #         # TODO new login info
    #         self.browser = Browser()
    #         # account['afs_token'] = self.browser.get_token()
    #         passport['afs_token'] = self.browser.afs_token
    #         user.update(passport)
    #         director = Director(user)
    #         # 运行
    #         director.run()
    #         # 回显
    #         if not director.tag:
    #             self.ui.table.setItem(i, 1, QTableWidgetItem('失败'))
    #             i += 1
    #             print('Director failed')
    #             continue
    #         # print(director.user.data)
    #         # TODO Encapsulate
    #         self.ui.table.setItem(i, 1, QTableWidgetItem(
    #             '完成' if director.wrong_info == []
    #             else '未完成打扫' if director.wrong_info == ['打扫']
    #             else '失败'))
    #         self.ui.table.setItem(i, 2, QTableWidgetItem(
    #             director.user.data['chickenCount']
    #             if director.user.has('chickenCount') else ''))
    #         self.ui.table.setItem(i, 3, QTableWidgetItem(
    #             director.user.data['eggCount']
    #             if director.user.has('eggCount') else ''
    #         ))
    #         if director.wrong_info == []:
    #             print(director.user.data['phone'] + ": " + "成功" +
    #                   " 兔子数：" + director.user.data['chickenCount'])
    #
    #         else:
    #             print(director.user.data['phone'] + ": " + "失败" + str(director.wrong_info) +
    #                   " 兔子数：" + director.user.data['chickenCount'])
    #         i += 1
    #     print('----- 结束 -----')

    def child_accept(self):
        flag = 1
        phone = self.child.LineEdit_account.text()
        pwd = self.child.LineEdit_password.text()

        if phone == '' or pwd == '':
            flag = 0

        for user in self.user_list:
            if user.find('phone') == phone:
                flag = 0
                break
        if self.child.checkBox_isTop.isChecked():
            is_top = 0
        else:
            is_top = 1
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
        if self.ui.radioButton.isChecked():
            self.timer.start(1800000)
            self.daily_timer.start((55800 - QDateTime.currentDateTime().toTime_t() % 86400) * 1000)
            print('daily timer:', self.daily_timer.remainingTime())
            self.weekly_timer.start((363600 - QDateTime.currentDateTime().toTime_t() % 604800) * 1000)
        else:
            self.timer.stop()
            self.daily_timer.stop()
            self.weekly_timer.stop()
    # deprecated
    # def refresh_table(self):
    #     current = len(self.passport_list)
    #     old = self.ui.table.rowCount()
    #     if current >= old:
    #         print('Now', current, 'users.')
    #         for row in range(0, current):
    #             # TODO delete
    #             # print(row, self.passport_list[row]['phone'])
    #             if row >= old:
    #                 self.ui.table.insertRow(row)
    #                 self.ui.table.setItem(row, 0, QTableWidgetItem(self.passport_list[row]['phone']))
    #                 # TODO delete
    #                 # print('set', self.ui.table.item(row, 0).text())
    #                 continue
    #             # 编辑
    #             # if phone != self.passport_list[row]:
    #     else:
    #         i_current = 0
    #         i_old = 0
    #         while i_old < self.ui.table.rowCount():
    #
    #             phone = self.ui.table.item(i_old, 0).text()
    #             if phone != self.passport_list[i_current]:
    #                 self.ui.table.removeRow(i_old)
    #             else:
    #                 i_old += 1
    #             i_current += 1


app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
