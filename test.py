# -*- coding: utf-8 -*-
# @Time    : 1/21/18 11:23 AM
# @Author  : Lester
from Director import Director
from user import User
import global_var as gv


def test():
    user = User()
    user.update(gv.passport_dic)
    director = Director(user)
    director.run()
    print(director.user.data.__class__)
    for key, val in director.user.data.items():
        print(key, val)
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


if __name__ == '__main__':
    test()
    # test_get_egg()