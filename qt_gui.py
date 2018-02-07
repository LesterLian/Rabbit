# -*- coding: utf-8 -*-
# @Time    : 1/30/2018 11:32 PM
# @Author  : Lester
import sys
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from PyQt5.QtWidgets import QMainWindow
from ui import Ui_MainWindow
from gui_popup2 import Ui_Dialog


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 主界面
        self.ui = Ui_MainWindow(self)
        self.ui.passport_list = []
        self.ui.add_passport = []
        try:
            self.ui.user_file = open('user', 'r')
            for line in self.ui.user_file.readlines():
                temp = line.split()
                self.ui.passport_list.append({'phone': temp[0], 'pwd': temp[1]})
                self.ui.user_file.close()
        except FileNotFoundError:
            print('User File Not Found')
            self.ui.user_file = open('user', 'w')
            self.ui.user_file.close()
        # 弹窗
        self.child = Ui_Dialog()
        # self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(lambda: self.add_button())

    def child_accept(self):
        flag = 1
        phone = self.child.lineEdit.text()
        pwd = self.child.lineEdit_2.text()
        for passport in self.ui.passport_list:
            if passport['phone'] == phone:
                flag = 0
                break
        if flag == 1:
            self.ui.passport_list.append({'phone': phone, 'pwd': pwd})
            self.ui.passport_list.append({'phone': phone, 'pwd': pwd})
            self.ui.table.insertRow(self.ui.table.rowCount())
            self.flash_table_passport()
            self.child.lineEdit.clear()
            self.child.lineEdit_2.clear()
            try:
                user_file = open('user', 'a+')
                user_file.write(phone + ' ' + pwd + '\n')
                user_file.close()
            except FileExistsError:
                print('file error')
            print('ok')
        else:
            print('重复passport')

    def add_button(self):
        self.child = Ui_Dialog()
        self.child.buttonBox.accepted.connect(self.child_accept)
        self.child.exec_()

    # 刷新table
    def flash_table_passport(self):
        self.ui.table.clearContents()
        print(self.ui.passport_list)
        i = 0
        for passport in self.ui.passport_list:
            self.ui.table.setItem(i, 0,
                                  QTableWidgetItem(passport['phone']))
            i += 1


app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
