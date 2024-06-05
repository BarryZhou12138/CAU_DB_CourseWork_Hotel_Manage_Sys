import DB.DB_control
import response.login
def Complete_food_order(food_id,username,password,connect:DB.DB_control.DB_connect):
    login_result,msg = response.login.login(username,password,'2',connect)
    if not login_result:
        return False,msg
    search_food_result = connect.search('点餐表',"点餐单号 = '%s'"%food_id)
    if len(search_food_result) == 0:
        return False,'没有该订单'
    else:
        connect.update('点餐表',"完成状态 = '已完成'","点餐单号 = '%s'"%food_id)
        return True,'成功修改'