# -*- coding: utf-8 -*-
# @Time    : 1/24/18 9:24 PM
# @Author  : Lester
from collections import OrderedDict
from abc import abstractmethod


class PostInterface:
    def __init__(self, user):
        self.user = user
        self.post_dict = OrderedDict()
        self.post_obj = None
        self.next_step = ''
        self.wrong_info = ''
        self.init_post_dict()
        self.post()
        print(self.next_step)
        if self.post_obj or self.post_obj.success:
            self.success()
            if self.next_step == '':
                raise ValueError('next_step needs to be set after success.')
        else:
            self.fail()
            if self.next_step == '' or self.wrong_info == '':
                raise ValueError('next_step and wrong_info needs to be set after fail')



    @abstractmethod
    def init_post_dict(self):
        pass

    @abstractmethod
    def post(self):
        pass

    @abstractmethod
    def success(self):
        pass

    @abstractmethod
    def fail(self):
        pass
