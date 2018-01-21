# -*- coding: utf-8 -*-
# @Time    : 1/19/18 4:27 PM
# @Author  : Lester
from post.PostInterface import PostInterface

class PostRatio(PostInterface):

    def set_post_url(self):
        self.post_url = 'HappyRabbit/message/getRatio'