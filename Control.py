# -*- coding: utf-8 -*-
# @Author  : Lester

#import POST
from post import PostLogin, manager
import global_var as gv

userList = dict()
tasks = gv.tasks
mng = manager.Manager()


def init(user_info):
    for info in user_info:
        userList[info[0]] = {"phone": info[0], "pwd": info[1]}

    mng.register(name="login", post_proto=PostLogin.PostLogin(gv.passport_dic, 'token'))


def add_user(phone, pwd):
    userList[phone] = {"phone": phone, "pwd": pwd}


def process():
    for user in userList:
        for command in tasks:
            executor = mng.create(command)
            executor.run()
            print(executor.get_response_dic())

            print(userList[user])
