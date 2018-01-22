# -*- coding: utf-8 -*-
# @Time    : 19/01/2018 10:14 AM
# @Author  : Akio

import global_var as gv
import requests
import strategies
from collections import OrderedDict


class Post:
    def __init__(self, command, post_keys, *return_keys):
        self.command = command
        self.post_keys = post_keys
        self.info_dict = dict()
        self.return_keys = return_keys
        self.response_json = None
        self.response_dic = {}
        self.tmp_dic = {}

    def set_info(self, user):
        #self.info_dict = info_dict
        self.info_dict = strategies.get_extra_keys(self.command, user)

    def run(self, user):
        # self.set_post_url()
        self.set_info(user)
        self.post(user)
        self.make_response_dic()
        print(self.tmp_dic)

    def post(self, user):
        url = gv.url + self.command

        user_info_dict = user.data.copy()  # don't update original dict
        user_info_dict.update(self.info_dict)
        ordered_dict = OrderedDict()
        for k in self.post_keys:
            ordered_dict[k] = user_info_dict[k]
        data = self.make_data(self.warp_dic(ordered_dict))

        self.response_json = requests.post(url, data=data, headers=gv.headers).json()

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
