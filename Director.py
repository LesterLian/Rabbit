# -*- coding: utf-8 -*-
# @Time    : 22/01/2018 2:39 PM
# @Author  : Akio
from post.post import *


class Director:
    def __init__(self, user):
        self.user = user
        self.next_step = 'login'
        self.wrong_num = 0
        self.tag = False
        self.wrong_info = []

    def run(self):
        while not (self.tag and self.wrong_num < 3):
            self.do_post()
        # l debug
        print('run() ends')

    def do_post(self):
        # l debug
        print(self.next_step)
        if self.next_step == 'login':
            self.login()
        elif self.next_step == 'getRatio':
            self.get_ratio()
        elif self.next_step == 'getFieldEggs':
            self.get_field_eggs()
        elif self.next_step == 'hatchField':
            self.hatch_field()
        elif self.next_step == 'cleanFriend':
            self.clean_friend()
        elif self.next_step == 'end':
            self.tag = True
        # l debug
        print(self.user.data)

    # 登陆
    def login(self):
        post_dict = OrderedDict()
        post_dict['phone'] = self.user.data['phone']
        post_dict['pwd'] = self.user.data['pwd']
        post_obj = Post('login', post_dict, 'userId', 'token')
        if post_obj.success:
            response_dic = post_obj.get_response_dic()
            self.user.update(response_dic)
            self.next_step = 'getRatio'
        else:
            self.wrong_num += 1
            self.wrong_info.append('login')
            self.next_step = 'login'

    # 获得利率
    def get_ratio(self):
        post_dict = OrderedDict()
        post_dict['userId'] = self.user.data['userId']
        post_dict['token'] = self.user.data['token']
        post_obj = Post('getRatio', post_dict, 'chickenCount')  # , 'ratios'
        if post_obj.success:
            response_dic = post_obj.get_response_dic()
            self.user.update(response_dic)
            self.next_step = 'getFieldEggs'
        else:
            self.wrong_num += 1
            self.wrong_info.append('getRatio')
            self.next_step = 'login'

    # 收小兔
    def get_field_eggs(self):
        # 如果想要fields需要先getFieldInfo
        self.get_field_info()
        fields_list = self.user.data['fields']
        for filed_info in fields_list:
            if filed_info['hasEgg'] == '1':
                post_dict = OrderedDict()
                post_dict['userId'] = self.user.data['userId']
                post_dict['fieldId'] = filed_info['id']
                post_dict['token'] = self.user.data['token']
                # 没有数据需要更新到user.data
                post_obj = Post('getFieldEggs', post_dict)
                if not post_obj.success:
                    self.wrong_info.append('getFieldEggs: ' + filed_info['id'])
        self.next_step = 'cleanFriend'

    # 收好友小兔
    def clean_friend(self):
        self.get_friend_list()
        if self.user.data['friends']:
            for friend in self.user.data['friends']:
                # 还没被清扫
                if friend['hasClean'] == '0':
                    post_dict = OrderedDict()
                    post_dict['userId'] = self.user.data['userId']
                    post_dict['fieldId'] = friend['userId']
                    post_dict['token'] = self.user.data['token']
                post_obj = Post('getFieldEggs', post_dict)
                if not post_obj.success:
                    # todo 重写错误信息格式
                    self.wrong_info.append('clean_friend: ' + post_dict['fieldId'] + post_obj.response_json)
        self.next_step = 'hatchField'

    # 获取好友列表
    def get_friend_list(self):
        post_dict = OrderedDict()
        post_dict['userId'] = self.user.data['userId']
        post_dict['token'] = self.user.data['token']
        post_obj = Post('getFriendList', post_dict, 'friends')
        if post_obj.success:
            response_dic = post_obj.get_response_dic()
            # 作为终端没有下一步指令，只update数据
            self.user.update(response_dic)
        else:
            self.wrong_num += 1
            self.wrong_info.append('getFieldInfo')

    # 增养小兔子
    def hatch_field(self):
        self.get_field_info()
        max_num = 3000
        # 对小兔取整数
        egg_count = int(float(self.user.data['eggCount']))
        fields_list = self.user.data['fields']
        for filed_info in fields_list:
            if filed_info['active'] and egg_count > 0:
                # 可以孵化位置数量
                blank_space = max_num - int(filed_info['chickens'])
                if blank_space > 0:
                    post_dict = OrderedDict()
                    add_count = egg_count if egg_count < blank_space else blank_space
                    egg_count -= add_count
                    post_dict['userId'] = self.user.data['userId']
                    post_dict['fieldId'] = filed_info['id']
                    post_dict['addCount'] = str(add_count)
                    post_dict['token'] = self.user.data['token']
                    # 没有数据需要更新到user.data
                    post_obj = Post('hatchField', post_dict)
                    if post_obj.success:
                        egg_count = int(float(self.user.data['eggCount']) - add_count)
                    else:
                        self.wrong_info.append('hatch_field: ' + filed_info['id'])
        self.next_step = 'end'  # todo 下一步是啥

    # 获取/更新 信息
    def get_field_info(self):
        post_dict = OrderedDict()
        post_dict['userId'] = self.user.data['userId']
        # 暂时不处理好友
        post_dict['friendId'] = ''
        post_dict['token'] = self.user.data['token']
        post_obj = Post('getFieldInfo', post_dict, 'chickenCount', 'eggCount', 'fields')
        if post_obj.success:
            response_dic = post_obj.get_response_dic()
            # 作为终端没有下一步指令，只update数据
            self.user.update(response_dic)
        else:
            self.wrong_num += 1
            self.wrong_info.append('getFieldInfo')

    # 判断success=='0'时候的处理方法可以根据response_json['message']来判断
    def post_fail(self, post_obj):
        message = post_obj.response_json['message']
        if message == '已超时，请重新登录':
            self.next_step = 'login'
