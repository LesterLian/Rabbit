import POST
userList = dict()
tasks = {"login", "getRatio", "getFieldInfo"}
# , "getFieldEggs", "getFieldInfo", "getHatchCount", "hatchField", "getFieldInfo"


def init(user_info):
    for info in user_info:
        userList[info[0]] = info[1]


def add_user(phone, pwd):
    userList[phone] = pwd


def process():
    for user in userList:
        for command in tasks:
            POST.post(user, command)
