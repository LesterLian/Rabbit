# -*- coding: utf-8 -*-
# @Author  : Lester

#import POST
from post.PostLogin import PostLogin
from post.manager import Manager
import global_var as gv

userList = dict()
tasks = gv.tasks
mng = Manager()


def init(user_info):
    for info in user_info:
        userList[info[0]] = {"phone": info[0], "pwd": info[1]}

    for command in gv.fields_dict:
        mng.register(command, PostLogin(command, *gv.fields_dict[command]))
    # mng.register(name="login", post_proto=PostLogin(['phone', 'pwd'], 'token', 'userId'))
    # mng.register(name='getRatio', post_proto=PostLogin(['userId', 'token']))



def add_user(phone, pwd):
    userList[phone] = {"phone": phone, "pwd": pwd}


def process():
    for user in userList:
        for command in tasks:
            executor = mng.create(command)
            executor.set_info(tasks[command])
            executor.run(userList[user])
            userList[user].update(executor.get_response_dic())

            print(executor.get_response_dic())
            print(userList[user])
