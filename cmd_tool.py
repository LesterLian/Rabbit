# -*- coding: utf-8 -*-
# @author Lester
from director import Director
from user import User

passport_list = []
user_file = None

try:
    user_file = open('user', 'r')
    for line in user_file.readlines():
        temp = line.split()
        passport_list.append({'phone': temp[0], 'pwd': temp[1]})
        user_file.close()
        user_file = open('user', 'a')
except FileNotFoundError:
    print('User File Not Found')
    user_file = open('user', 'w')
command = ''
while not command == 'run':
    command = input('Enter command: ')
    if command == 'add':
        phone = input('Enter Phone: ')
        pwd = input('Enter Password: ')
        passport_list.append({
            'phone': phone,
            'pwd': pwd})
        try:
            user_file.write(phone + ' ' + pwd + '\n')
        except:
            print('Write File Error')
            exit(1)
user_file.close()
for passport in passport_list:
    user = User()
    user.update(passport)
    director = Director(user)
    director.run()
    # print(director.user.data)
    if director.wrong_info == []:
        print(director.user.data['phone'] + ": " + "成功" +
              " 兔子数：" + director.user.data['chickenCount'] +
              " 兔仔数: " + director.user.data['eggCount'])
    else:
        print(director.user.data['phone'] + ": " + "失败" + str(director.wrong_info) +
              " 兔子数：" + director.user.data['chickenCount'] +
              " 兔仔数: " + director.user.data['eggCount'])
