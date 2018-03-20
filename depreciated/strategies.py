# -*- coding: utf-8 -*-
# @Time    : 1/21/18 11:49 AM
# @Author  : Lester
from global_var import tasks


# def get_extra_keys(command, user):
#     if command == 'getFieldInfo':
#         return {'friendId': ""}  # for test only, should be implemented in other ways
#     elif command == 'getFieldEggs':
#         re = {'fieldIdList': []}
#         for field in user.get('fields'):
#             if field['active'] == '1':
#                 re['hasEgg'] = '1'
#                 re['fieldIdList'] += [field['id']]
#         user.update(re)
#         return re
#     elif command == 'getHatchCount':
#         if user.get('hasEgg') == '1':
#
#     elif command == 'hatchField':
