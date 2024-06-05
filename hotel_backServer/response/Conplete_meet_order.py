import DB.DB_control
import response.login
def Complete_meet_order(meet_id,meet_type,username,password,connect:DB.DB_control.DB_connect):
    login_result,msg = response.login.login(username,password,'2',connect)

    if not login_result:
        return False,msg

    if meet_type == '接':
        table_name = '接站预约表'
        id_name = '接站订单编号'
    elif meet_type == '送':
        table_name = '送站预约表'
        id_name = '送站订单编号 '
    else:
        return False,'接送类型输入错误'

    search_food_result = connect.search(table_name,"%s = '%s'"%(id_name,meet_id))

    if len(search_food_result) == 0:
        return False,'没有该订单'
    else:
        connect.update(table_name, "完成状态 = '已完成'", "%s = '%s'" % (id_name, meet_id))
        return True, '成功修改'