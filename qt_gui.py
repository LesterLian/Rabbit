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
        self.ui = Ui_MainWindow(self)
        self.child = Ui_Dialog()
        # self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(lambda: self.add_button())

    def add_button(self):
        self.child = Ui_Dialog()
        self.child.buttonBox.accepted.connect(self.additem)
        self.child.exec_()

    def additem(self):
        phone = self.child.lineEdit.text()
        # pwd = self.child.lineEdit_2.text()
        self.ui.table.insertRow(self.ui.table.rowCount())
        self.ui.table.setItem(self.ui.table.rowCount() - 1, 0, QTableWidgetItem(phone))
        self.child.lineEdit.clear()
        self.child.lineEdit_2.clear()
app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
