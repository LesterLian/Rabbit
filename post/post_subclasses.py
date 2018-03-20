# -*- coding: utf-8 -*-
# @Time    : 1/24/18 9:38 PM
# @Author  : Lester
from post.post_interface import PostInterface
from post.post import Post


class Login(PostInterface):
    def __init__(self, user, log):
        super(Login, self).__init__(user, log)

    def post(self):
        self.post_obj = Post('login', self.post_dict, 'userId', 'token')
        self.check()

    def init_post_dict(self):
        self.post_dict['phone'] = self.user.get('phone')
        self.post_dict['pwd'] = self.user.get('pwd')
        self.post_dict["afs_scene"] = "login"
        self.post_dict["afs_token"] = self.user.get('afs_token')
        self.post_dict["type"] = '1'

    def success(self):
        response_dic = self.post_obj.get_response_dic()
        self.user.update(response_dic)
        self.next_step = 'getRatio'

    def fail(self):
        self.wrong_info = '登录'
        self.next_step = 'login'
        self.log.log(self.post_obj)
        

class GetRatio(PostInterface):
    def __init__(self, user, log):
        super(GetRatio, self).__init__(user, log)

    def init_post_dict(self):
        self.post_dict['userId'] = self.user.get('userId')
        self.post_dict['token'] = self.user.get('token')

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
    def __init__(self, user, log):
        GetFieldInfo(user, log)
        super(GetFieldEggs, self).__init__(user, log)

    def init_post_dict(self):
        self.post_dict['userId'] = self.user.get('userId')
        self.post_dict['fieldId'] = 'need id'
        self.post_dict['token'] = self.user.get('token')

    def post(self):
        self.check()  # Must be called.
        self.successful = True
        fields_list = self.user.get('fields')

        for filed_info in fields_list:
            if filed_info['hasEgg'] == '1':
                print('hasEgg')
                self.post_dict['fieldId'] = filed_info.get('id')
                self.post_obj = Post('getFieldEggs', self.post_dict)
                self.check()

        # TODO check logic
        # sleep

    def success(self):
        self.next_step = 'cleanFriend'

    def fail(self):
        self.wrong_info = '收兔'
        self.next_step = 'cleanFriend'  # TODO check logic
        self.log.log(self.post_obj)


class HatchField(PostInterface):
    def __init__(self, user, log):
        GetFieldInfo(user, log)
        super(HatchField, self).__init__(user, log)

    def init_post_dict(self):
        self.post_dict['userId'] = self.user.get('userId')
        self.post_dict['fieldId'] = 'need id'
        self.post_dict['addCount'] = 'need count'
        self.post_dict['token'] = self.user.get('token')

    def post(self):
        # 对小兔取整数
        egg_count = int(float(self.user.get('eggCount')))
        fields_list = self.user.get('fields')
        self.check()
        self.successful = True
        for filed_info in fields_list:
            if egg_count > 0 and filed_info['active'] == '1':
                # 可以孵化位置数量
                blank_space = (3000 if len(filed_info.get('id')) == 1 else 20000) - int(filed_info['chickens'])
                if blank_space > 0:
                    add_count = egg_count if egg_count < blank_space else blank_space
                    self.post_dict['fieldId'] = filed_info.get('id')
                    self.post_dict['addCount'] = str(add_count)
                    self.post_obj = Post('hatchField', self.post_dict)
                    # 如果post成功更新egg_count
                    # TODO 成功检测失误
                    if not self.check():
                        self.log.log(self.post_obj)
                    else:
                        egg_count -= add_count
        # TODO check logic
        # sleep

    def success(self):
        self.next_step = 'end'  # todo 下一步是啥

    def fail(self):
        self.wrong_info = '孵化'
        self.next_step = 'end'  # todo 下一步是啥


class CleanFriend(PostInterface):
    def __init__(self, user, log):
        GetFriendList(user, log)
        super(CleanFriend, self).__init__(user, log)

    def init_post_dict(self):
        self.post_dict['userId'] = self.user.get('userId')
        self.post_dict['friendId'] = 'need friend id'
        self.post_dict['token'] = self.user.get('token')

    def post(self):
        self.check()  # Must be called.
        self.successful = True
        all_successful = True

        if self.user.get('friends'):
            for friend in self.user.get('friends'):
                self.successful = True
                # 还没被清扫
                if friend['hasClean'] == '0':
                    self.post_dict['friendId'] = friend.get('userId')
                    self.post_obj = Post('cleanFriend', self.post_dict)
                    if not self.check():
                        all_successful = False
                        self.log.log(self.post_obj)
            self.successful = all_successful
        # l debug
        # print('clean', self.successful)

    def success(self):
        self.next_step = 'hatchField'

    def fail(self):
        self.wrong_info = '打扫'
        self.next_step = 'hatchField'


class GetFriendList(PostInterface):
    def __init__(self, user, log):
        super(GetFriendList, self).__init__(user, log)

    def init_post_dict(self):
        self.post_dict['userId'] = self.user.get('userId')
        self.post_dict['token'] = self.user.\
            get('token')

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
    def __init__(self, user, log):
        super(GetFieldInfo, self).__init__(user, log)

    def init_post_dict(self):
        self.post_dict['userId'] = self.user.get('userId')
        # 好友信息是拜访用的
        self.post_dict['friendId'] = ''
        self.post_dict['token'] = self.user.get('token')

    def post(self):
        self.post_obj = Post('getFieldInfo', self.post_dict, 'chickenCount', 'eggCount', 'fields')
        self.check()

    # TODO handle failure
    def success(self):
        response_dic = self.post_obj.get_response_dic()
        # 作为终端没有下一步指令，只update数据
        self.user.update(response_dic)
        self.next_step = 'None'

    def fail(self):
        self.wrong_info = '兔场'
        self.next_step = 'None'
