import DB.DB_control
import response.login
def change_room(username, password, order_id, room_id, connect:DB.DB_control.DB_connect):

    login_result, msg = response.login.login(username, password, '2', connect)
    if not login_result:
        return False, msg

    search_result = connect.search('订单表', "订单编号='%s'" % order_id)
    if len(search_result) == 0:
        return False, '查无此订单'

    search_login = connect.search('入住登记表', "订单编号='%s'" % order_id)
    if len(search_login) == 0:
        return False, '该订单还没入住，不允许换房'

    search_room = connect.search('房间表'," 房型号='%s' and 房间号 = '%s' and 使用状态='空'"%(search_result[0][2],room_id))
    if len(search_room)==1:
        connect.update('房间表', "使用状态 = '空'", " 房间号='%s'" % search_login[0][2])
        connect.update('房间表',"使用状态 = '满'"," 房间号='%s'"%room_id)
        return True,'修改成功'
    else:
        return False,'该房间已经入住'