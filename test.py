# -*- coding: utf-8 -*-
# @Time    : 1/21/18 11:23 AM
# @Author  : Lester
from Director import Director
from user import User
import global_var as gv
if __name__ == '__main__':
    user = User()
    user.update(gv.passport_dic)
    director = Director(user)
    director.run()
    print(director.user.data.__class__)
    for key, val in director.user.data.items():
        print(key, val)
    print('over')
