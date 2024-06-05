import DB.DB_control
import response.login
def delete_order_by_staff(username,password,order_id,connect:DB.DB_control.DB_connect):

    login_result, msg = response.login.login(username, password, '2', connect)
    if not login_result:
        return False, msg

    search_result = connect.search('订单表',"订单编号='%s'"%order_id)
    if len(search_result) == 0:
        return False,'查无此订单'

    search_login = connect.search('入住登记表', "订单编号='%s'" % order_id)
    if len(search_login) == 1:
        return False, '该订单已经入住，删除失败'

    connect.delete('订单表',"订单编号='%s'"%order_id)
    return True,'删除成功'