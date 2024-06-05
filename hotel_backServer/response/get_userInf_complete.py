def get_userInf_complete(username, password, connecter):
    print("get_userInf_complete "+username+" "+password)
    search_result = connecter.search('用户表', "用户名='%s'"%username)
    if len(search_result)==1:
        if search_result[0][9]==password:
           for i in range(10):
               if search_result[0][i] is None:
                    break
           if i<9:
              return False,'信息有空缺'
           else:
               return True,'信息完整'
        else:
            return False, '密码错误'
    else:
        return False,'用户未注册'
        

    