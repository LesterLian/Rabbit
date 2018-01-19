# -*- coding: utf-8 -*-
# @Author  : Lester

import POST
import global_var as gv

userList = dict()
tasks = gv.tasks


def init(user_info):
    for info in user_info:
        userList[info[0]] = {"phone": info[0], "pwd": info[1]}


def add_user(phone, pwd):
    userList[phone] = {"phone": phone, "pwd": pwd}


def process():
    for user in userList:
        for command in tasks:
            userList[user].update(POST.post(userList[user], command))
            print(userList[user])
