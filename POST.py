# -*- coding: utf-8 -*-
# @Time    : 18/01/2018 3:38 PM
# @Author  : Akio
import requests
import collections


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
    site = ""
    headers = {'Host': site,
               'Connection': 'keep-alive',
               'Content-Length': '69',
               'Origin': 'http://' + site,
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': '*/*',
               'Referer': 'http://' + site,
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               #'Cookie': 'JSESSIONID=7A0C06FEECC0791C617246454E0F5C8C; SERVERID=f87be926a52270b7c7946ea3fc002737|1516243416|1516242845'
               }
    url = 'http://' + site + '/HappyRabbit/message/' + command
    log_dic = collections.OrderedDict()
    log_dic["phone"] = "17702201060"
    log_dic["pwd"] = "111111"
    log_data = make_data(get_info(user, command))
    # d = {'data': "{\"phone\": \"17702201060\", \"pwd\": \"111111\"}"}
    r = requests.post(url, data=log_data)
    print(r.text)
