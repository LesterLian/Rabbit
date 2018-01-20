# -*- coding: utf-8 -*-
# @Time    : 19/01/2018 10:14 AM
# @Author  : Akio

import global_var as gv
import requests
from abc import abstractmethod


class PostInterface:
    def __init__(self, command, field_list, *find_keys):
        self.command = command
        self.field_list = field_list  # list contains field names needed for POST
        self.info_dict = dict()
        self.get_keys = find_keys
        self.response_json = None
        self.response_dic = {}
        self.tmp_dic = {}

    def set_info(self, info_dict):
        self.info_dict = info_dict

    def run(self, user_info_dict):
        self.set_post_url()
        self.post(user_info_dict)
        self.make_response_dic()
        print(self.tmp_dic)

    def post(self, user_info_dict):  # adds a variable to make interface general for multiple users
        url = gv.url + self.command  # changed to receive command instead
        user_info_dict.update(self.info_dict)
        data = self.make_data(self.warp_dic({k: user_info_dict[k] for k in self.field_list}))
        self.response_json = requests.post(url, data=data, headers=gv.headers).json()

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
        self.json2dic(self.response_json)
        for find_key in self.get_keys:
            self.response_dic[find_key] = self.tmp_dic[find_key]

    def json2dic(self, json):  # TODO puts repeated info into set instead of updating them.
        for key, val in json.items():
            if isinstance(val, dict):
                self.json2dic(val)
            else:
                self.tmp_dic[key] = val

    @abstractmethod
    def set_post_url(self):
        pass
