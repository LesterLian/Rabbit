# -*- coding: utf-8 -*-
# @Time    : 24/01/2018 2:08 PM
# @Author  : Akio

from appJar import gui

def launch(win):
    app.showSubWindow(win)

app=gui()

# this is a pop-up
app.startSubWindow("one", modal=True)
app.addLabel("l1", "SubWindow One")
app.stopSubWindow()

# this is another pop-up
app.startSubWindow("two")
app.addLabel("l2", "SubWindow Two")
app.stopSubWindow()

# these go in the main window
app.addButtons(["one", "two"], launch)


# add labels & entries
app.addLabelSecretEntry('password', 0, 0)
app.addLabelNumericEntry('f', 1, 0)
app.addLabelOptionBox('y', [1, 2, 3], 1, 3)


app.go()