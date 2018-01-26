# -*- coding: utf-8 -*-
# @Time    : 1/24/18 9:24 PM
# @Author  : Lester
from collections import OrderedDict
from abc import abstractmethod


class PostInterface:
    """
    next_step must be set
    check() must be called at least once and when every post occurs
    """
    def __init__(self, user, log):
        self.log = log
        self.user = user
        self.post_dict = OrderedDict()
        self.post_obj = None
        self.next_step = ''
        self.wrong_info = ''
        self.successful = True
        self.checked = 0

        self.init_post_dict()
        self.post()
        if self.checked == 0:
            raise SyntaxError('check() has not been called')
        if self.successful:
            self.success()
            if self.next_step == '':
                raise ValueError('next_step needs to be set after success.')
        else:
            self.fail()
            if self.next_step == '' or self.wrong_info == '':
                raise ValueError('next_step and wrong_info needs to be set after fail')
        print(self.next_step)

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

    def check(self):
        self.successful = self.successful and (self.post_obj and self.post_obj.success)
        self.checked += 1
