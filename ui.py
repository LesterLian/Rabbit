# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QDialog
from user import User
from director import Director
from gui_popup import Ui_Dialog


class Ui_MainWindow(object):
    def __init__(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 400)
        MainWindow.setMinimumSize(QtCore.QSize(800, 400))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 800, 231))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 800, 229))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.table = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.table.setGeometry(QtCore.QRect(0, 0, 800, 231))
        self.table.setObjectName("tableView")
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['账号', '状态', '兔子数', '兔仔数'])
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 250, 56, 21))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 250, 56, 21))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(80, 250, 56, 21))
        self.pushButton_3.setObjectName("pushButton_3")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(420, 250, 61, 23))
        self.radioButton.setObjectName("radioButton")
        self.timer = QtCore.QTimer()
        self.dialog = Ui_Dialog(QDialog())

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)

        self.user_file = None
        self.passport_list = []
        try:
            self.user_file = open('user', 'r')
            for line in self.user_file.readlines():
                temp = line.split()
                self.passport_list.append({'phone': temp[0], 'pwd': temp[1]})
                self.table.insertRow(self.table.rowCount())
                self.table.setItem(self.table.rowCount()-1, 0, QTableWidgetItem(temp[0]))
                self.user_file.close()
        except FileNotFoundError:
            print('User File Not Found')
            self.user_file = open('user', 'w')
            self.user_file.close()
        self.radioButton.setChecked(True)
        self.timer.start(1800000)

        self.pushButton.clicked.connect(lambda: self.add_button())
        self.pushButton_2.clicked.connect(lambda: self.run_button())
        self.pushButton_3.clicked.connect(lambda: self.delete_button())
        self.timer.timeout.connect(lambda: self.pushButton_2.click())
        self.radioButton.toggled.connect(lambda: self.timer_switch())
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AutoRabbit"))
        self.pushButton.setText(_translate("MainWindow", "添加"))
        self.pushButton_2.setText(_translate("MainWindow", "开始"))
        self.pushButton_3.setText(_translate("MainWindow", "删除"))
        self.radioButton.setText(_translate("MainWindow", "定时"))

    def timer_switch(self):
        if self.radioButton.isChecked():
            self.timer.start(1800000)
        else:
            self.timer.stop()

    def add_button(self):
        self.dialog.show()

        # # TODO real add
        # phone = '17702201060'
        # pwd = '111111'
        # self.user_file = open('user', 'a')
        # self.user_file.write(phone + ' ' + pwd + '\n')
        # self.passport_list = [{'phone': phone, 'pwd': pwd}] + self.passport_list
        #
        # self.table.insertRow(0)
        # self.table.setItem(0, 0, QTableWidgetItem(phone))
        # self.user_file.close()

    def delete_button(self):
        # TODO implement
        return

    def run_button(self):
        self.user_file.close()
        i = 0
        for passport in self.passport_list:
            user = User()
            user.update(passport)
            director = Director(user)
            director.run()
            if not director.tag:
                self.table.setItem(i, 1, QTableWidgetItem('失败'))
                i += 1
                print('Director failed')
                continue
            # print(director.user.data)
            # TODO Encapsulate
            self.table.setItem(i, 1, QTableWidgetItem(
                 '完成' if director.wrong_info == []
                 else '未完成打扫' if director.wrong_info == ['打扫']
                 else '失败'))
            self.table.setItem(i, 2, QTableWidgetItem(
                director.user.data['chickenCount']
                if director.user.has('chickenCount') else ''))
            self.table.setItem(i, 3, QTableWidgetItem(
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
