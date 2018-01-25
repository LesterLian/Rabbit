# -*- coding: utf-8 -*-
# @Time    : 1/24/18 9:38 PM
# @Author  : Lester
from post.post_interface import PostInterface
from post.post import Post


class Login(PostInterface):

    def __init__(self, user):
        super(Login, self).__init__(user)

    def post(self):
        self.post_obj = Post('login', self.post_dict, 'userId', 'token')

    def init_post_dict(self):
        self.post_dict['phone'] = self.user.data.get('phone')
        self.post_dict['pwd'] = self.user.data.get('pwd')

    def success(self):
        response_dic = self.post_obj.get_response_dic()
        self.user.update(response_dic)
        self.next_step = 'end'

    def fail(self):
        self.wrong_info = '登录'
        self.next_step = 'end'

class GetRatio(PostInterface):

    def init_post_dict(self):
        pass

    def post(self):
        pass

    def success(self):
        pass

    def fail(self):
        pass