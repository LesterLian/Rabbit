# -*- coding: utf-8 -*-
# @Time    : 22/01/2018 2:39 PM
# @Author  : Akio
from post.post import *


class Director:
    def __init__(self, user):
        self.user = user
        self.next_step = 'login'
        self.wrong_num = 0
        self.tag = False

    def run(self):
        while not (self.tag and self.wrong_num < 3):
            self.do_post()

    def do_post(self):
        if self.next_step == 'login':
            self.login()
        if self.next_step == 'getRatio':
            self.get_ratio()

    def login(self):
        post_dict = OrderedDict()
        post_dict['phone'] = self.user.data['phone']
        post_dict['pwd'] = self.user.data['pwd']
        post_obj = Post('login', post_dict, 'userId', 'token')
        post_obj.run()
        if post_obj.success == '1':
            response_dic = post_obj.get_response_dic()
            self.user.update(response_dic)
            self.next_step = 'getRatio'
        else:
            self.wrong_num += 1
            self.next_step = 'login'

    def get_ratio(self):
        post_dict = OrderedDict()
        post_dict['userId'] = self.user.data['userId']
        post_dict['token'] = self.user.data['token']
        post_obj = Post('getRatio', post_dict, )  # todo 添加感兴趣的元素
        if post_obj.success == '1':
            response_dic = post_obj.get_response_dic()
            self.user.update(response_dic)
            self.next_step = 'getFieldInfo'
        else:
            self.wrong_num += 1
            self.next_step = 'login'

    def get_field_eggs(self):
        fields_list = self.user.data['fields']
        for filed_info in fields_list:
            if filed_info['hasEgg'] == 1:
                post_dict = OrderedDict()
                post_dict['userId'] = self.user.data['userId']
                post_dict['fieldId'] = filed_info['fieldId']
                post_dict['token'] = self.user.data['token']
                post_obj = Post()# todo 参数
                if post_obj.success == '1':
                    pass

