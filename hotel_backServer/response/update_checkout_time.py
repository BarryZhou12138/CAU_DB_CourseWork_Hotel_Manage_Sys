import DB.DB_control
import response.login
def update_checkout_time(username, password, order_id, check_out_time, connect:DB.DB_control.DB_connect):


    login_result, msg = response.login.login(username, password, '2', connect)
    if not login_result:
        return False, msg

    search_result = connect.search('订单表', "订单编号='%s'" % order_id)
    if len(search_result) == 0:
        return False, '查无此订单'

    connect.update('订单表',"预计离开日期 = '%s'"%check_out_time, "订单编号 = '%s'"%order_id)
    connect.update('入住登记表', "预计离开日期 = '%s'" % check_out_time, "订单编号 = '%s'" % order_id)
    return True,'更改成功'