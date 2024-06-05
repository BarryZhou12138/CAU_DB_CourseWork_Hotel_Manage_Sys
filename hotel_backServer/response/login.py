import pandas

def login(username,  password, loginType, connecter):

    print("login_callback "+username+" "+password+" "+loginType)

    if loginType == '1':
        search_result = connecter.search('用户表',"用户名='%s'"%(username))
        if len(search_result) == 1:
            if search_result[0][9] == password:
                return True,'登录成功'
            else:
                return False,'用户名或者密码错误'
        else:
            return False,'没有该用户，请先注册'

    elif loginType == '2':
        search_result = connecter.search('服务人员表',"服务人员联系电话='%s'"%(username))
        if len(search_result) == 1:
            if search_result[0][3] == password:
                return True,'登录成功'
            else:
                return False,'用户名或者密码错误'
        else:
            return False,'没有该服务员'

    elif loginType == '3':
        adminAccout = pandas.read_csv("admin.txt",header=None)
        if username == adminAccout[0][0] and password == adminAccout[0][1]:
            return True,'登录成功'
        else:
            return False,'登录失败'

    else:return False