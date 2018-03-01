# -*- coding: utf-8 -*-
# @Time    : 1/30/2018 11:32 PM
# @Author  : Lester
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import QDateTime, QTimer
from ui import Ui_MainWindow
from gui_popup2 import Ui_Dialog
from user import User
from director import Director
from webkit import Browser


class AppWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        # 主界面
        self.ui = Ui_MainWindow(self)

        # 读取用户文件
        self.passport_list = []
        self.user_file = None

        try:
            self.user_file = open('user', 'r')
            for line in self.user_file.readlines():
                temp = line.split()
                self.passport_list.append({'phone': temp[0], 'pwd': temp[1]})
                # self.ui.table.insertRow(self.ui.table.rowCount())
                # self.ui.table.setItem(self.ui.table.rowCount() - 1, 0, QTableWidgetItem(temp[0]))

                self.user_file.close()
        except FileNotFoundError:
            print('User File Not Found')
            self.user_file = open('user', 'w')
            self.user_file.close()
        print('refresh')
        self.refresh_table()
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
        self.ui.pushButton.clicked.connect(lambda: {self.child.exec_(), self.refresh_table()})
        self.ui.pushButton_2.clicked.connect(lambda: self.run_button())
        self.ui.pushButton_3.clicked.connect(lambda: self.delete_button())
        self.child.buttonBox.accepted.connect(self.child_accept)
        self.timer.timeout.connect(lambda: self.ui.pushButton_2.click())
        self.daily_timer.timeout.connect(lambda: {self.ui.pushButton_2.click(), self.daily_timer.start(86400000)})
        # self.weekly_timer.timeout.connect(lambda: {self.ui.pushButton_2.click(), self.weekly_timer.start(604800000)})
        self.ui.radioButton.toggled.connect(lambda: self.timer_switch())

    def delete_button(self):
        indices = self.ui.table.selectedIndexes()
        rows = list()
        for index in indices:
            row = index.row()
            append = True
            for row_num in rows:
                if row_num == row:
                    append = False
            if append:
                rows.insert(0, index.row())
        for row in rows:
            self.ui.table.removeRow(row)
            self.passport_list.pop(row)

        self.user_file = open('user', 'w')
        for passport in self.passport_list:
            self.user_file.write(passport['phone'] + ' ' + passport['pwd'] + '\n')
            # TODO delete
            # print(passport['phone'] + ' ' + passport['pwd'])
        self.user_file.close()
        # TODO delete
        # print(rows)
        return

    def run_button(self):
        self.user_file.close()
        i = 0

        for passport in self.passport_list:
            if self.ui.table.item(i, 1).text() == '完成' if self.ui.table.item(i, 1) else False:
                print('跳过')
                continue
            user = User()
            # TODO new login info
            # self.browser = Browser()
            # passport['afs_token'] = self.browser.get_token()
            user.update(passport)
            director = Director(user)
            director.run()
            if not director.tag:
                self.ui.table.setItem(i, 1, QTableWidgetItem('失败'))
                i += 1
                print('Director failed')
                continue
            # print(director.user.data)
            # TODO Encapsulate
            self.ui.table.setItem(i, 1, QTableWidgetItem(
                '完成' if director.wrong_info == []
                else '未完成打扫' if director.wrong_info == ['打扫']
                else '失败'))
            self.ui.table.setItem(i, 2, QTableWidgetItem(
                director.user.data['chickenCount']
                if director.user.has('chickenCount') else ''))
            self.ui.table.setItem(i, 3, QTableWidgetItem(
                director.user.data['eggCount']
                if director.user.has('eggCount') else ''
            ))
            if director.wrong_info == []:
                print(director.user.data['phone'] + ": " + "成功" +
                      " 兔子数：" + director.user.data['chickenCount'])

            else:
                print(director.user.data['phone'] + ": " + "失败" + str(director.wrong_info) +
                      " 兔子数：" + director.user.data['chickenCount'])
            i += 1
        print('----- 结束 -----')

    def child_accept(self):
        flag = 1
        phone = self.child.lineEdit.text()
        pwd = self.child.lineEdit_2.text()
        for passport in self.passport_list:
            if passport['phone'] == phone:
                flag = 0
                break
        if flag == 1:
            self.passport_list.append({'phone': phone, 'pwd': pwd})
            # self.ui.table.insertRow(self.ui.table.rowCount())
            # self.flash_table_passport()
            self.child.lineEdit.clear()
            self.child.lineEdit_2.clear()
            self.child.lineEdit.setFocus(0)
            try:
                user_file = open('user', 'a+')
                user_file.write(phone + ' ' + pwd + '\n')
                user_file.close()
            except FileExistsError:
                print('file error')
            print('ok')
        else:
            print('重复passport')

    # def add_button(self):
    #     self.child = Ui_Dialog()
    #     self.child.buttonBox.accepted.connect(self.child_accept)
    #     self.child.exec_()

    def timer_switch(self):
        if self.ui.radioButton.isChecked():
            self.timer.start(1800000)
            self.daily_timer.start((16200 - QDateTime.currentDateTime().toTime_t() % 86400) * 1000)
            # self.weekly_timer.start((525600 - QDateTime.currentDateTime().toTime_t() % 604800) * 1000)
        else:
            self.timer.stop()
            self.daily_timer.stop()
            # self.weekly_timer.stop()

    # 刷新table
    def flash_table_passport(self):
        self.ui.table.clearContents()
        print(self.passport_list)
        i = 0
        for passport in self.passport_list:
            self.ui.table.setItem(i, 0,
                                  QTableWidgetItem(passport['phone']))
            i += 1

    def refresh_table(self):
        current = len(self.passport_list)
        old = self.ui.table.rowCount()
        if current >= old:
            print('Now', current, 'users.')
            for row in range(0, current):
                # TODO delete
                # print(row, self.passport_list[row]['phone'])
                if row >= old:
                    self.ui.table.insertRow(row)
                    self.ui.table.setItem(row, 0, QTableWidgetItem(self.passport_list[row]['phone']))
                    # TODO delete
                    # print('set', self.ui.table.item(row, 0).text())
                    continue
                # 编辑
                # if phone != self.passport_list[row]:
        else:
            i_current = 0
            i_old = 0
            while i_old < self.ui.table.rowCount():

                phone = self.ui.table.item(i_old, 0).text()
                if phone != self.passport_list[i_current]:
                    self.ui.table.removeRow(i_old)
                else:
                    i_old += 1
                i_current += 1



app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
