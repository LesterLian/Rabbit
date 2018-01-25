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
        self.check()

    def init_post_dict(self):
        self.post_dict['phone'] = self.user.data.get('phone')
        self.post_dict['pwd'] = self.user.data.get('pwd')

    def success(self):
        response_dic = self.post_obj.get_response_dic()
        self.user.update(response_dic)
        self.next_step = 'getRatio'

    def fail(self):
        self.wrong_info = '登录'
        self.next_step = 'login'


class GetRatio(PostInterface):
    def __init__(self, user):
        super(GetRatio, self).__init__(user)

    def init_post_dict(self):
        self.post_dict['userId'] = self.user.data.get('userId')
        self.post_dict['token'] = self.user.data.get('token')

    def post(self):
        self.post_obj = Post('getRatio', self.post_dict, 'chickenCount')  # , 'ratios'
        self.check()

    def success(self):
        response_dic = self.post_obj.get_response_dic()
        self.user.update(response_dic)
        self.next_step = 'getFieldEggs'

    def fail(self):
        self.wrong_info = '首页'
        self.next_step = 'login'


class GetFieldEggs(PostInterface):
    def __init__(self, user):
        GetFieldInfo(user)
        super(GetFieldEggs, self).__init__(user)

    def init_post_dict(self):
        self.post_dict['userId'] = self.user.data.get('userId')
        self.post_dict['fieldId'] = 'need id'
        self.post_dict['token'] = self.user.data.get('token')

    def post(self):
        count = 0
        fields_list = self.user.data['fields']
        for filed_info in fields_list:
            if filed_info['hasEgg'] == '1':
                count += 1
                self.post_dict['fieldId'] = filed_info.get('id')
                self.post_obj = Post('getFieldEggs', self.post_dict)
                self.check()
        self.check()
        # TODO check logic
        if count == 0:
            self.successful = True

    def success(self):
        self.next_step = 'cleanFriend'

    def fail(self):
        self.wrong_info = '收兔'
        self.next_step = 'cleanFriend'  # TODO check logic


class HatchField(PostInterface):
    def __init__(self, user):
        GetFieldInfo(user)
        super(HatchField, self).__init__(user)
        self.max_num = 3000  # 黄地上限更高

    def init_post_dict(self):
        self.post_dict['userId'] = self.user.data.get('userId')
        self.post_dict['fieldId'] = 'need id'
        self.post_dict['addCount'] = 'need count'
        self.post_dict['token'] = self.user.data.get('token')

    def post(self):
        max_num = 3000
        # 对小兔取整数
        egg_count = int(float(self.user.data['eggCount']))
        fields_list = self.user.data['fields']
        active_count = 0
        for filed_info in fields_list:
            if egg_count > 0 and filed_info['active']:
                active_count += 1
                # 可以孵化位置数量
                blank_space = max_num - int(filed_info['chickens'])
                if blank_space > 0:
                    add_count = egg_count if egg_count < blank_space else blank_space
                    egg_count -= add_count
                    self.post_dict['fieldId'] = filed_info.get('id')
                    self.post_dict['addCount'] = str(add_count)
                    self.post_obj = Post('hatchField', self.post_dict)
                    # TODO logic
                    self.check()
        self.check()
        # TODO check logic
        if active_count == 0:
            self.successful = True

    def success(self):
        self.next_step = 'end'  # todo 下一步是啥

    def fail(self):
        self.wrong_info = '孵化'
        self.next_step = 'end'  # todo 下一步是啥


class CleanFriend(PostInterface):
    def __init__(self, user):
        GetFriendList(user)
        super(CleanFriend, self).__init__(user)

    def init_post_dict(self):
        self.post_dict['userId'] = self.user.data.get('userId')
        self.post_dict['friendId'] = 'need friend id'
        self.post_dict['token'] = self.user.data.get('token')

    def post(self):
        if self.user.data['friends']:
            for friend in self.user.data['friends']:
                # 还没被清扫
                if friend['hasClean'] == '0':
                    self.post_dict['friendId'] = friend.get('userId')
                    self.post_obj = Post('cleanFriend', self.post_dict)
                    self.check()
        self.check()

    def success(self):
        self.next_step = 'hatchField'

    def fail(self):
        self.wrong_info = '打扫'
        self.next_step = 'hatchField'


class GetFriendList(PostInterface):
    def __init__(self, user):
        super(GetFriendList, self).__init__(user)

    def init_post_dict(self):
        self.post_dict['userId'] = self.user.data.get('userId')
        self.post_dict['token'] = self.user.data.get('token')

    def post(self):
        self.post_obj = Post('getFriendList', self.post_dict, 'friends')
        self.check()

    def success(self):
        response_dic = self.post_obj.get_response_dic()
        # 作为终端没有下一步指令，只update数据
        self.user.update(response_dic)
        self.next_step = 'None'

    def fail(self):
        self.wrong_info = '好友'
        self.next_step = 'None'


class GetFieldInfo(PostInterface):
    def __init__(self, user):
        super(GetFieldInfo, self).__init__(user)

    def init_post_dict(self):
        self.post_dict['userId'] = self.user.data.get('userId')
        # 好友信息是拜访用的
        self.post_dict['friendId'] = ''
        self.post_dict['token'] = self.user.data.get('token')

    def post(self):
        self.post_obj = Post('getFieldInfo', self.post_dict, 'chickenCount', 'eggCount', 'fields')
        self.check()

    def success(self):
        response_dic = self.post_obj.get_response_dic()
        # 作为终端没有下一步指令，只update数据
        self.user.update(response_dic)
        self.next_step = 'None'

    def fail(self):
        self.wrong_info = '兔场'
        self.next_step = 'None'

