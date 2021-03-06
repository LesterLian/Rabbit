# -*- coding: utf-8 -*-
# @Time    : 24/01/2018 12:47 PM
# @Author  : Akio
import time
from appJar import gui
from director import Director
from user import User
from post.post import *
from tomorrow3 import threads

pools_flag = 0


# 感觉没效果
# @threads(100)
def press(btn_name):
    global pools_flag
    pools_flag = 1

    if btn_name == '添加':
        app.showSubWindow('password_box')
    if btn_name == 'ok':
        phone = str(int(app.getEntry('帐号')))
        pwd = app.getEntry('密码')
        passport = OrderedDict()
        passport['phone'] = phone
        passport['pwd'] = pwd
        passport_list.append(passport)
        app.addListItem('账户信息', phone)
        app.clearEntry("帐号")
        app.clearEntry("密码")
    if btn_name == '删除':
        position = app.getListBoxPos('账户信息')[0]
        app.removeListItemAtPos('账户信息', position)
        passport_list.pop(position)
    if btn_name == '开始':
        try:
            user_file = open('user', 'w', encoding='utf8')
            for passport in passport_list:
                user_file.write(passport['phone'] + ' ' + passport['pwd'] + '\n')
            user_file.close()
        except:
            print('Write File Error')
        app.disableButton('开始')
        app.clearListBox("处理结果")
        for passport in passport_list:
            run(passport)
        # delete
        print('-------结束----------')
        app.enableButton('开始')


# @threads(2)  # app.addListItem may need block
def run(passport):
    user = User()
    user.update(passport)
    director = Director(user)
    director.run()
    # delete
    print(director.user.data)
    if director.wrong_info == []:
        passport = director.user.data['phone'] + ": " + "成功" + \
                   " 兔子数：" + director.user.data['chickenCount'] + \
                   " 兔仔数: " + director.user.data['eggCount']
    else:
        passport = director.user.data['phone'] + ": " + "失败" + str(director.wrong_info) + \
                   " 兔子数：" + director.user.data['chickenCount'] + \
                   " 兔仔数: " + director.user.data['eggCount']
    app.addListItem('处理结果', passport)
    # time.sleep(1)


def do_pools():
    global pools_flag
    if pools_flag == 1:
        press('开始')


# def check_time():


# create the GUI & set a title
app = gui("AutoRabbit", "600x300")

passport_list = []
# passport_list = gv.passport_list
try:
    user_file = open('user', 'r', encoding='utf8')
    for line in user_file.readlines():
        temp = line.split()
        passport_list.append({'phone': temp[0], 'pwd': temp[1]})
        user_file.close()
except FileNotFoundError:
    print('File Not Found')

show_info = []
for item in passport_list:
    show_info.append(item['phone'])
# delete
print(show_info)
app.addListBox('账户信息', show_info, 0, 0, 1, 3)
app.addListBox('处理结果', [], 0, 1, 3, 3)
app.addButtons(['添加',
                '删除',
                '开始'],
               press, 3, 0, 2, 1
               )
app.addCheckBox('定时', 3, 3)
# app.addNumericLabelEntry('时间', None, 3, 4)
app.setStretch("none")
# app.after(1800000, do_pools)
# app.after(60000, check_time)
# pop-up
app.startSubWindow('password_box', "添加账户", modal=True)
app.addLabelNumericEntry('帐号', 0, 0)
app.addLabelEntry('密码', 1, 0)
app.addButtons(["ok"], press, 2, 0)
app.stopSubWindow()

app.go()

# 修改帐号功能
