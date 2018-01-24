# -*- coding: utf-8 -*-
# @Time    : 23/01/2018 3:20 PM
# @Author  : Akio
from collections import OrderedDict
import requests
import global_var as gv


class Post:
    # post_dict ordered
    def __init__(self, command, post_dict, *return_keys):
        self.command = command
        self.post_dict = post_dict
        self.return_keys = return_keys
        self.response_json = None
        self.response_dic = {}
        self.tmp_dic = {}
        self.success = False
        self.run()
    def run(self):
        # self.set_post_url()
        self.post()
        self.make_response_dic()

    def post(self):
        url = gv.url + self.command
        data = self.make_data(self.warp_dic(self.post_dict))
        self.response_json = requests.post(url, data=data, headers=gv.headers).json()
        # ximi
        # print(self.response_json['success'], self.response_json['message'])
        self.success = self.response_json['success'] == '1'
        return self.response_json['success'] == '0'

    @staticmethod
    def warp_dic(dic_t):
        re = "{"
        for key, val in dic_t.items():
            re += "\"" + str(key) + "\":" + "\"" + str(val) + "\","
        re = re[:-1] + "}"

        return re

    @staticmethod
    def make_data(dic_string):
        re = {
            'data': dic_string
        }
        return re

    def get_response_dic(self):
        return self.response_dic

    def make_response_dic(self):
        # 只有当post成功时候才往response_dic里写数据
        if self.response_json['success'] == '1':
            self.json2dic(self.response_json)
            for key in self.return_keys:
                self.response_dic[key] = self.tmp_dic[key]

    def json2dic(self, json):  # TODO Maybe put repeated info into set instead of updating them.
        for key, val in json.items():
            if isinstance(val, dict):
                self.json2dic(val)
            else:
                self.tmp_dic[key] = val

    # @abstractmethod
    # def set_post_url(self):
    #     pass
