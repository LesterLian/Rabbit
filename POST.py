# -*- coding: utf-8 -*-
# @Time    : 18/01/2018 3:38 PM
# @Author  : Akio
import requests
import collections
import global_var as gv


post_format = {"login": {"phone", "pwd"}}


def get_info(user, command):
    re = "{"
    for field in post_format[command]:
        re += "\"" + field + "\":" + "\"" + user[field] + "\","
    re = re[:-1] + "}"

    return re


def warp_dic(dic_t):
    re = "{"
    for key, val in dic_t.items():
        re += "\"" + str(key) + "\":" + "\"" + str(val) + "\","
    re = re[:-1] + "}"

    return re


def make_data(dic_string):
    re = {
        'data': dic_string
    }
    return re


def post(user, command):
    site = gv.site
    url = 'http://' + site + '/HappyRabbit/message/' + command
    log_data = make_data(get_info(user, command))
    r = requests.post(url, data=log_data)
    print(r.text)

# def json2dic(json, *keys):
#     dic = collections.OrderedDict()
#     for key in keys:
#         if key in json.keys():
#             dic['key'] = json['key']
#         else:
#             for json_key in json.keys():
#                 if

