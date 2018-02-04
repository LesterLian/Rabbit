# -*- coding: utf-8 -*-
# @Time    : 1/30/2018 11:32 PM
# @Author  : Lester
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from ui import Ui_MainWindow


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow(self)
        # self.ui.setupUi(self)
        self.show()


app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
