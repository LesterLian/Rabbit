# -*- coding: utf-8 -*-
# @Time    : 19/01/2018 9:05 AM
# @Author  : Lian
import POST
import global_var as gv

userList = dict()
tasks = gv.tasks


def init(user_info):
    for info in user_info:
        userList[info[0]] = info[1]


def add_user(phone, pwd):
    userList[phone] = pwd


def process():
    for user in userList:
        for command in tasks:
            POST.post(user, command)
