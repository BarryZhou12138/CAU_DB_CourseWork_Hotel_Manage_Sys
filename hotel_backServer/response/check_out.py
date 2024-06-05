import datetime

def check_out(username, password, checkout_date, damage_fee, damage_description, order_id, staff_id, connecter):
    print("check_out " + username + " " + password + " " + checkout_date + " " + damage_fee + " " + damage_description + " " + order_id + " " + staff_id)
    
    search_result = connecter.search('服务人员表', "服务人员联系电话='%s'" % username)
    
    if search_result is not None:
     if len(search_result) == 1:
        if search_result[0][3] == password:
            search_order_id = connecter.search('订单表', "订单编号='%s'" % order_id)
            
            if len(search_order_id) == 0:
                return False, '订单编号有误'
            
            search_check_in_date = connecter.search('入住登记表', "订单编号='%s'" % order_id)
            
            if len(search_check_in_date) == 0:
                return False, '还未入住'
            
            search_price = connecter.search('房型表', "房型号='%s'" % search_order_id[0][2])
            
            if len(search_price) == 0:
                return False, '房型号有误'
            
            search_check_in = search_check_in_date[0][5]
            check_in_date = search_check_in.date()
            check_out_date = datetime.datetime.strptime(checkout_date[:10], "%Y-%m-%d").date()
            actual_stay_cost = (check_out_date - check_in_date).days * float(search_price[0][2])
            connecter.update('房间表',"使用状态='空'","房间号='%s'"%search_check_in_date[0][2])
            connecter.insert('退房登记表(退房日期,损坏费用,损坏情况描述,订单编号,服务人员联系电话,实际住宿费用)',
                             "('%s','%s','%s','%s','%s','%s')" % (checkout_date, damage_fee, damage_description, order_id, staff_id, actual_stay_cost))
            

            userID=search_order_id[0][1]
            search_food_cost=connecter.search('点餐表', "订单编号='%s'" % order_id)
            food_cost=0
            if len(search_food_cost)==0:
               food_cost=0
            else:
               n=len(search_food_cost)
               for i in range(0,n):
                  x = connecter.search('餐单表',"套餐编号 = '%s'"%search_food_cost[i][3])
                  food_cost=float(x[0][3])+food_cost

            search_meet_cost=connecter.search('接站预约表', "订单编号='%s'" % order_id)
            meet_cost=0
            if len(search_meet_cost)==0:
               meet_cost=0
            else:
               n=len(search_meet_cost)
               for i in range(0,n):
                    x = connecter.search('接送类型表', "接送形式编码 = '%s'" % search_meet_cost[i][1])
                    food_cost = float(x[0][2]) + meet_cost

            search_send_cost=connecter.search('送站预约表', "订单编号='%s'" % order_id)
            send_cost=0
            if len(search_send_cost)==0:
               send_cost=0
            else:
               n=len(search_send_cost)
               for i in range(0,n):
                   x = connecter.search('接送类型表', "接送形式编码 = '%s'" % search_send_cost[i][1])
                   food_cost = float(x[0][2]) + send_cost
            total_cost=float(actual_stay_cost)+float(food_cost)+float(meet_cost)+float(damage_fee)+float(send_cost)-float(search_order_id[0][6])-float(search_order_id[0][6])
            connecter.insert('账单表(订单编号,用户ID,服务人员编号,实际住宿费用,预计住宿费用,点餐费用,损坏费用,接站费用,送站费用,押金,总费用,退房日期)',
                             "('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (order_id, userID, staff_id, actual_stay_cost,search_order_id[0][6],food_cost,damage_fee, meet_cost,send_cost,search_check_in_date[0][6],total_cost,checkout_date))
            
            return True,total_cost
        else:
            return False, '服务人员密码错误'
     else:
        return False, '服务人员姓名输入错误'
    else:
    # 处理查询结果为空的情况
      return False, '未找到服务人员记录'