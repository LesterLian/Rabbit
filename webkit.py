# -*- coding: utf-8 -*-
# @Time    : 2/23/18 4:02 PM
# @Author  : Lester

from PyQt5.QtCore import QUrl, QRect
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QPushButton
import sys
import time


# class MyBrowser(QWebPage):
#     ''' Settings for the browser.'''
#
#     def userAgentForUrl(self, url):
#         ''' Returns a User Agent that will be seen by the website. '''
#         return "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"


class Browser(QWebEngineView):
    def __init__(self):
        super(QWebEngineView, self).__init__()
        # self.view = QWebEngineView.__init__(self)
        # self.setUrl(QUrl())
        self.afs_token = ''
        self.page = self.page()
        self.load(QUrl("https://jixiangtukeji.com/rabbit/login/index.html?next=0"))

        self.loadFinished.connect(lambda: {self.run_js(), print('run_js returned')})

        # self.pushButton = QPushButton(self.window())
        # self.pushButton.setGeometry(QRect(0, 0, 56, 21))
        # self.pushButton.setObjectName("pushButton")
        # self.pushButton.setText("Push")
        # self.pushButton.clicked.connect(lambda: self.get_token())

    def run_js(self):
        self.page.runJavaScript('pointman.getConfig().token', lambda r: self.process_token(r))

    def process_token(self, r):
        # TODO 保证获取token
        print('r:', r)
        self.afs_token = r if r else ''

    def get_token(self):
        return self.afs_token

    def disableJS(self):
        settings = QWebEngineSettings.globalSettings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, False)


# app = QApplication(sys.argv)
# view = Browser()
#
# view.show()
# app.exec()
