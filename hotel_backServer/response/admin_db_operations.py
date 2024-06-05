import response.login
import traceback
def admin_db_operations(admin,password,sql,connecter):
    print("admin_operation "+admin+" "+password+" "+sql)
    result,msg = response.login.login(admin,password,'3',connecter)
    #登录验证
    if not result:
        return result,'登录失败'
    try:
        data = connecter.direct_execute(sql)
        return True,data
    except Exception as e:
        return False,traceback.format_exc()