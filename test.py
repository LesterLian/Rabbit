# -*- coding: utf-8 -*-
# @Time    : 1/21/18 11:23 AM
# @Author  : Lester
from Director import Director
from user import User
import global_var as gv
from post.post import *
import json


def test():
    user = User()
    user.update(gv.passport_dic)
    # user.update(passport)
    director = Director(user)
    director.run()
    print(director.wrong_info)
    print('over')


def test_get_egg():
    user = User()
    user.data = {'phone': '17702201060', 'pwd': '111111', 'userId': '4e41b114-25cd-46e0-a6ce-19b864922a20',
                 'token': '426c14a7-9b38-42fd-aa26-69750f533226'}
    director = Director(user)
    director.login()
    director.get_ratio()
    director.get_field_eggs()
    print(user.data, '\n', director.wrong_info)


def test_hatch_field():
    user = User()
    user.data = {'phone': '17702201060', 'pwd': '111111', 'userId': '4e41b114-25cd-46e0-a6ce-19b864922a20',
                 'token': '426c14a7-9b38-42fd-aa26-69750f533226'}
    director = Director(user)
    director.login()
    director.get_ratio()
    director.hatch_field()
    print(user.data, '\n', director.wrong_info)


def test_fiend():
    user = User()
    user.update(gv.passport_dic)
    director = Director(user)
    director.login()
    test_dict = OrderedDict()
    test_dict['userId'] = director.user.data['userId']
    test_dict['friendId'] = '2b822135-a1b7-429c-be41-4ca6a30a3916'
    test_dict['token'] = director.user.data['token']
    post_obj = Post('cleanFriend',
                    test_dict,
                    )
    print(post_obj.response_json)
    post_obj = Post('cleanFriend', test_dict)
    print(post_obj.response_json)


if __name__ == '__main__':
    # test()
    # test_fiend()
    print('a'.__class__ is str)
