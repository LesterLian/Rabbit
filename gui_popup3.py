# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'popup.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog


class Ui_Dialog(QDialog):
    def __init__(self, parent=None):
        super(Ui_Dialog, self).__init__(parent)
        self.setObjectName("Dialog")
        self.resize(400, 160)
        self.ButtonBox = QtWidgets.QDialogButtonBox(self)
        self.ButtonBox.setGeometry(QtCore.QRect(150, 120, 231, 32))
        self.ButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.ButtonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Close | QtWidgets.QDialogButtonBox.Ok)
        self.ButtonBox.setObjectName("buttonBox")
        self.LineEdit_account = QtWidgets.QLineEdit(self)
        self.LineEdit_account.setGeometry(QtCore.QRect(70, 20, 311, 31))
        self.LineEdit_account.setObjectName("lineEdit")
        self.LineEdit_password = QtWidgets.QLineEdit(self)
        self.LineEdit_password.setGeometry(QtCore.QRect(70, 70, 311, 31))
        self.LineEdit_password.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(20, 20, 41, 19))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 41, 19))
        self.label_2.setObjectName("label_2")
        self.checkBox_isTop = QtWidgets.QCheckBox(self)
        self.checkBox_isTop.setGeometry(QtCore.QRect(30, 120, 91, 31))
        self.checkBox_isTop.setObjectName("checkBox")

        self.retranslateUi(self)
        # self.ButtonBox.accepted.connect(self.accept)
        self.ButtonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "账号"))
        self.label_2.setText(_translate("Dialog", "密码"))
        self.checkBox_isTop.setText(_translate("Dialog", "是否为下线"))
