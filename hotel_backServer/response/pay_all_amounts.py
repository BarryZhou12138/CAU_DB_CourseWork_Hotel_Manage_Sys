def pay_all_amounts(username,password,order_id,connecter):
    print("pay_all_amounts " + username + " " + password + " " +order_id)
    search_result = connecter.search('用户表', "用户名='%s'" % username)
    if len(search_result)==1:
        if search_result[0][9]==password:
            search_order_id=connecter.search('订单表',"订单编号='%s'"%order_id)
            if len(search_order_id)==0:
                return False,'订单不存在'
            else:
                if search_order_id[0][7]=='未支付': 
                     order_cost=float(search_order_id [0][6])
                     connecter.update('订单表',"定金支付状态='已支付'","订单编号='%s'"%order_id)
                else:
                     order_cost=0
                search_food_id=connecter.search('点餐表',"订单编号='%s'"%order_id)
                if len(search_food_id)==0:
                    food_cost=0
                else:
                    n=len(search_food_id)
                    for i in range(0,n):
                        if search_food_id[i][9]=='未完成':
                            food_cost=food_cost+float(search_food_id[i][6])
                            connecter.update('点餐表',"完成状态='已完成'","点餐单号='%s'"%search_food_id[i][0])
                search_meet_id=connecter.search('接站预约表',"订单编号='%s'"%order_id)
                if len(search_meet_id)==0:
                    meet_cost=0
                else:
                    n=len(search_meet_id)
                    for i in range(0,n):
                        if search_meet_id[i][5]=='未完成':
                            search_meet_cost=connecter.search('接送形式表',"接送形式编码='%s'"%search_meet_id[i][1])
                            meet_cost=meet_cost+float(search_meet_cost[i][2])
                            connecter.update('接站预约表',"完成状态='已完成'","接站订单编号='%s'"%search_meet_id[i][0])
                search_send_id=connecter.search('送站预约表',"订单编号='%s'"%order_id)
                if len(search_send_id)==0:
                    send_cost=0
                else:
                    n=len(search_send_id)
                    for i in range(0,n):
                        if search_send_id[i][5]=='未完成':
                            search_send_cost=connecter.search('接送形式表',"接送形式编码='%s'"%search_send_id[i][1])
                            send_cost=send_cost+float(search_send_cost[i][2])
                            connecter.update('送站预约表',"完成状态='已完成'","送站订单编号='%s'"%search_send_id[i][0])
                total_pay=order_cost+food_cost+meet_cost+send_cost
                return True,'所有未完成的支付全部支付成功'

        else:
            return False,'密码输入错误'
    else:
        return False,'用户还未注册'
