# -*- coding: utf-8 -*-
# @Time    : 19/01/2018 5:15 PM
# @Author  : Akio


# class Director:
#     def __init__(self, post_obj):
#         self.post_obj = post_obj
#
#     def run(self):
#         self.post_obj.set_post_url()
#         self.post_obj.post()
#         self.post_obj.make_response_dic()
#
#     def get_response_dic(self):
#         return self.post_obj.response_dic


# passport_list = gv.passport_list
# for passport in passport_list:
#     user = User()
#     user.update(passport)
#     director = Director(user)
#     director.run()
# "register", '{"sex":"' + t + '","nickName":"' + this.nickNameTF.text + '",
# "realName":"' + this.realNameTF.text + '","wechat":"123456","alipay":"123456",
# "pwd":"' + this.pwdTF.text + '","phone":"' + this.phoneTF.text + '","phoneCode":"' + this.codeTF.text + '","invitationCode":"' + this.invitationCodeTF.text + '"}'
# data = OrderedDict()
# data['sex'] = '0'
# data['nickName'] = '李应1233'
# data['realName'] = '李应'
# data['wechat'] = '123456'
# data['alipay'] = '123456'
#
# data['phone'] = '17702201061'
# data['pwd'] = '111111'
# data['phoneCode'] = '6670'
# data['invitationCode'] = '1211606'
# # data['userId'] = '4e41b114-25cd-46e0-a6ce-19b864922a20'
# data = Post.make_data(Post.warp_dic(data))
# response = requests.post('http://jixiangtukeji.com/HappyRabbit/message/register',
#                          data=data, headers=gv.headers)
# print('-----------------info-----------------')
# print(response.status_code)
# print('-----------------info-----------------')
# print(response.content)
# print('-----------------info-----------------')
# print(response.text)
# print('-----------------info-----------------')
