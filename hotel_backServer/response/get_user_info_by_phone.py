import DB.DB_control
import response.login
def get_user_info_by_phone(username,password,phone,connect:DB.DB_control.DB_connect):

    login_result, msg = response.login.login(username, password, '2', connect)
    if not login_result:
        return False, msg

    user_imf = connect.search('用户表',"联系电话 = '%s'"%phone)

    if len(user_imf)==0:
        return False,'查无此人'

    return True,user_imf