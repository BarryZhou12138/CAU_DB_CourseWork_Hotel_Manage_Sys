def remove_order(username, password, order_id,connecter):
    print("remove_order "+username+" "+password+" "+order_id)
    search_result = connecter.search('用户表', "用户名='%s'"%username)
    search_order_id=connecter.search('入住登记表', "订单编号='%s'"%order_id)
    if len(search_result)==1:
        if search_result[0][9]==password:
            if len(search_order_id)==0:
                connecter.delete('订单表',"订单编号='%s'"%order_id)
                return True,'删除订单成功'
            else:
                return False,'已经入住，无法删除'
        else:
            return False,'密码错误'
    else:
        return False,'还未注册'
