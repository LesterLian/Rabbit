# -*- coding: utf-8 -*-
# @Author  : Lester
from appJar import gui
import global_var as gv


strings = gv.ui_str


def init_gui():
    app = gui()
    app.start
    app.addLabelEntry(strings[0])
    app.addLabelEntry(strings[1])

    app.go()


if __name__ == '__main__':
    init_gui()
    # Control.init(gv.passport_list)
    # Control.process()

