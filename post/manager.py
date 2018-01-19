# -*- coding: utf-8 -*-
# @Time    : 19/01/2018 10:04 AM
# @Author  : Akio


class Manager:
    def __init__(self):
        self.showcase = {}

    def register(self, name, post_proto):
        self.showcase[name] = post_proto

    def create(self, post_proto_name):
        return self.showcase[post_proto_name]
