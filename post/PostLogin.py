# -*- coding: utf-8 -*-
# @Time    : 19/01/2018 1:35 PM
# @Author  : Akio
from post.PostInterface import PostInterface
import global_var as gv

class PostLogin(PostInterface):

    def set_post_url(self):
        self.post_url = 'HappyRabbit/message/login'


if __name__ == '__main__':
    Pl = PostLogin(gv.passport_dic,
                   'token')
    Pl.run()
    print(Pl.get_response_dic())
