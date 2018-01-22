# -*- coding: utf-8 -*-
# @Author  : Lester

from post.post import Post
from post.manager import Manager
from user import User
import global_var as gv

userDict = dict()
tasks = gv.tasks
mng = Manager()


def init(user_info):
    for info in user_info:
        # userDict[info[0]] = {"phone": info[0], "pwd": info[1]}
        add_user(info[0], info[1])

    for command in gv.post_init_dict:
        mng.register(command, Post(command, *gv.post_init_dict[command]))
    # mng.register(name="login", post_proto=PostLogin(['phone', 'pwd'], 'token', 'userId'))
    # mng.register(name='getRatio', post_proto=PostLogin(['userId', 'token']))


def add_user(phone, pwd):
    new_user = User()
    new_user.update({'phone': phone, 'pwd': pwd})
    userDict[phone] = new_user


def process():
    for user_phone in userDict:
        for command in tasks:
            executor = mng.create(command)

            # executor.set_info(tasks[command])

            if executor.run(userDict[user_phone]):  # maybe encapsulate, but how?
                print("Post Error")
                return
            userDict[user_phone].update(executor.get_response_dic())

            print(executor.get_response_dic())
            print(userDict[user_phone].data)
