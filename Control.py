# -*- coding: utf-8 -*-
# @Author  : Lester

from post.post import Post
from post.manager import Manager
from user import User
from Director import Director
import global_var as gv

userDict = dict()
tasks = gv.tasks
mng = Manager()


def init(user_info):
    for info in user_info:
        # userDict[info[0]] = {"phone": info[0], "pwd": info[1]}
        add_user(info[0], info[1])

    # for command in gv.post_init_dict:
    #     mng.register(command, Post(command, *gv.post_init_dict[command]))


def add_user(phone, pwd):
    new_user = User()
    new_user.update({'phone': phone, 'pwd': pwd})
    userDict[phone] = new_user


def process():
    for phone, user in userDict.items():
        director = Director(user)
        director.run()
        print(director.user.data.__class__)
        for key, val in director.user.data.items():
            print(key, val)
# def process():
#     for user_phone in userDict:
#         for command in tasks:
#             executor = mng.create(command)
#
#             # executor.set_info(tasks[command])
#
#             if executor.run(userDict[user_phone]):  # maybe encapsulate, but how?
#                 print("Post Error")
#                 return
#             userDict[user_phone].update(executor.get_response_dic())
#
#             print(executor.get_response_dic())
#             print(userDict[user_phone].data)
