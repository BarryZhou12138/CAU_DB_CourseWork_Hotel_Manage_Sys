import datetime

def get_food_orders(date, username, password, connecter):
    print("get_food_orders " + date + " " + username + " " + password)
    search_result = connecter.search('服务人员表', "服务人员联系电话='%s'" % username)
    if len(search_result) == 1:
        if password == search_result[0][3]:
            search_all_orders = connecter.search('点餐表', "送餐时间<='%s'" % date)
            result_data=[]
            n=len(search_all_orders)
            if n==0:
                return False,'此日期前没有点餐的客户'
            else:
                 for i in range(0,n):
                     if search_all_orders[i][9]=='未完成':
                        delivery_time=search_all_orders[i][4]
                        delivery_time=delivery_time.strftime('%Y-%m-%d %H:%M')
                        search_useID= connecter.search('订单表', "订单编号='%s'" % search_all_orders[i][3])
                        if len(search_useID)==0:
                           return False,'订单编号有误'
                        else:
                           search_usernames= connecter.search('用户表', "用户ID='%s'" % search_useID[0][1])
                           if len(search_usernames)==1:
                             search_food=connecter.search('餐单表', "套餐编号='%s'" %  search_all_orders[i][2])
                             if len(search_food)==1:
                               result_data.append(
                               {
                                'order_id': search_all_orders[i][3],
                                'username':search_usernames[0][2],
                                'dish_name':search_food[0][2],
                                'dish_type': search_food[0][1],
                                'dish_taste': search_all_orders[i][7],
                                'delivery_time': delivery_time
                                })
                             else:
                                 return False,'套餐编号有误'
                           else:
                               return False,'用户ID有误'  
                 return True,result_data

        else:
            return False, '密码输入错误'
    else:
        return False, '不存在该服务人员'