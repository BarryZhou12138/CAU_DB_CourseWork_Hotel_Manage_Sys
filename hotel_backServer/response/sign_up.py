from nanoid import generate

def sign_up(username, password, connecter):
    print("signUp_callback " + username + " " + password)
    if len(username)<8 or len(password)<8 or len(username)>15 or len(password)>15:
        return False,'用户名或者密码长度不正确'
    search_result = connecter.search('用户表', "用户名='%s'"%username)
    temp_ID = generate(size=8)
    if len(search_result) == 0:
        connecter.insert('用户表(用户ID,用户名,登录密码)',"('%s','%s','%s')"%(temp_ID,username,password))
        return True,'注册成功'
    else:
        return False,'当前用户名已经注册'
