# -*- coding: utf-8 -*-
# @Time    : 18/01/2018 3:38 PM
# @Author  : Akio
import requests
import json
import global_var as gv


post_format = {"login": ["phone", "pwd"],
               "getRatio": ["userId", "token"]
               }
return_format = {"login": [["user", "userId"], "token"],
                 "getRatio": []
                 }


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
    response = requests.post(url, data=log_data)
    r_obj = json.loads(response.text)
    re = dict()

    if r_obj["success"] == "0":
        return re

    for field in return_format[command]:
        if isinstance(field, list):
            re[field[1]] = r_obj[field[0]][field[1]]
        else:
            re[field] = r_obj[field]
    print(response.text)
    return re

# def json2dic(json, *keys):
#     dic = collections.OrderedDict()
#     for key in keys:
#         if key in json.keys():
#             dic['key'] = json['key']
#         else:
#             for json_key in json.keys():
#                 if

