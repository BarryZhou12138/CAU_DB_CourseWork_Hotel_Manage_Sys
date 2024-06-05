import datetime

def get_order_ids(array, index):
    return set([item[index] for item in array])
def get_checkin_orders(date, username, password, connecter):
    print("get_checkin_orders " + date + " " + username + " " + password)
    search_result = connecter.search('服务人员表', "服务人员联系电话='%s'" % username)
    if len(search_result) == 1:
        if password == search_result[0][3]:
            search_all_orders = connecter.search('订单表', "预计入住日期<='%s'" % date)
            search_out_orders = connecter.search('退房登记表',"退房日期<='%s'"% date)
            search_doing_orders= connecter.search('入住登记表',"入住日期<='%s'"% date)
            all_order_ids = get_order_ids(search_all_orders,0)
            out_order_ids = get_order_ids(search_out_orders,3)
            doing_order_ids = get_order_ids(search_doing_orders,0)

            result_order_ids = all_order_ids - out_order_ids - doing_order_ids

            # 根据订单编号从原始数组中获取完整的订单信息
            result = [order for order in search_all_orders if order[0] in result_order_ids and order[0] not in out_order_ids]
            result_data=[]
            n=len(result)
            if n==0:
                return False,'此日期前没有应入住但还未入住的客户'
            else:
                 for i in range(0,n):
                     search_usernames=connecter.search('用户表', "用户ID='%s'" % result[i][1])
                     if len(search_usernames)==1:
                         usernames=search_usernames[0][1]
                     else:
                         return False,'搜查结果有误'
                     search_room_type=connecter.search('房型表', "房型号='%s'" % result[i][2])
                     if len(search_room_type)==1:
                         room_type=search_room_type[0][1]
                     else:
                         return False,'搜查结果有误'
                     check_in = result[i][4].strftime('%Y-%m-%d')  # 将日期对象转换为字符串
                     check_out = result[i][5].strftime('%Y-%m-%d')  # 将日期对象转换为字符串
                     result_data.append(
                            {
                                'order_id': result[i][0],
                                'real_name':search_usernames[0][2],
                                'phone':search_usernames[0][7],
                                'room_id':search_room_type[0][0],
                                'username': usernames,
                                'room_type': room_type,
                                'check_in': check_in,
                                'check_out': check_out
                            })
                 return True,result_data

        else:
            return False, '密码输入错误'
    else:
        return False, '不存在该服务人员'