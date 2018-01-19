# -*- coding: utf-8 -*-
# @Time    : 19/01/2018 10:14 AM
# @Author  : Akio

import global_var as gv
import requests
from abc import abstractmethod


class PostInterface:
    def __init__(self, info_dic, *find_keys):
        self.post_url = ""
        self.info_dic = info_dic
        self.get_keys = find_keys
        self.response_json = None
        self.response_dic = {}
        self.tmp_dic = {}

    def run(self):
        self.set_post_url()
        self.post()
        self.make_response_dic()
        print(self.tmp_dic)

    def post(self):
        url = gv.url + self.post_url
        data = self.make_data(self.warp_dic(self.info_dic))
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

    def json2dic(self, json):
        for key, val in json.items():
            if isinstance(val, dict):
                self.json2dic(val)
            else:
                self.tmp_dic[key] = val

    @abstractmethod
    def set_post_url(self):
        pass
