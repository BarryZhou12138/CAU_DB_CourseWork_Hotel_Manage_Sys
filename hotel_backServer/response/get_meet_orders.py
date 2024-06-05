import datetime

def get_order_ids(array, index):
    return set([item[index] for item in array])
def get_meet_orders(date, username, password, connecter):
    print("get_meet_orders " + date + " " + username + " " + password)
    search_result = connecter.search('服务人员表', "服务人员联系电话='%s'" % username)
    if len(search_result) == 1:
        if password == search_result[0][3]:
            search_all_orders_a = connecter.search('接站预约表', "接站日期<='%s' and 完成状态='未完成'" % date)
            search_all_orders_b = connecter.search('送站预约表', "送站日期<='%s' and 完成状态='未完成'" % date)
            m=len(search_all_orders_a)
            n=len(search_all_orders_b)
            result_data=[]
            if (m==0 and n==0):
                return False,'此日期前没有需要接送的客户'
            else:
                 if m!=0:
                  for i in range(0,m):
                     if search_all_orders_a[i][5]=='未完成':
                       search_useID= connecter.search('订单表', "订单编号='%s'" % search_all_orders_a[i][2])
                       if len(search_useID)==0:
                           return False,'订单编号有误'
                       else:
                           search_usernames= connecter.search('用户表', "用户ID='%s'" % search_useID[0][1])
                           if len(search_usernames)==1:
                                    search_meet_type=connecter.search('接送类型表', "接送形式编码='%s'" % search_all_orders_a[i][1])
                                    if len(search_meet_type)==1:
                                        meet_type=search_meet_type[0][1]
                                        meet_date=search_all_orders_a[i][3].date()
                                        meet_time=search_all_orders_a[i][3].time()
                                        meet_date_str=meet_date.strftime('%Y-%m-%d')
                                        meet_time_str=meet_time.strftime('%H:%M')
                                        result_data.append(
                                           {
                                            'order_id': search_all_orders_a[i][0],
                                            'username': search_usernames[0][1],
                                            'meet_type': meet_type,
                                            'meet_date': meet_date_str,
                                            'meet_time': meet_time_str,
                                            'meet_location': search_all_orders_a[i][4],
                                            'real_name':search_usernames[0][2],
                                            'phone':search_usernames[0][7],
                                            'meet_action':"接站"
                                               })
                                    else:
                                        return False,'接送形式编码有误'
                           else:
                               return False,'用户ID有误'
                 if n!=0:
                  for i in range(0,n):
                     if search_all_orders_b[i][5]=='未完成':
                       search_useID= connecter.search('订单表', "订单编号='%s'" % search_all_orders_b[i][2])
                       if len(search_useID)==0:
                           return False,'订单编号有误'
                       else:
                           search_usernames= connecter.search('用户表', "用户ID='%s'" % search_useID[0][1])
                           if len(search_usernames)==1:
                                    search_meet_type=connecter.search('接送类型表', "接送形式编码='%s'" % search_all_orders_b[i][1])
                                    if len(search_meet_type)==1:
                                        meet_type=search_meet_type[0][1]
                                        meet_date=search_all_orders_b[i][3].date()
                                        meet_time=search_all_orders_b[i][3].time()
                                        meet_date_str=meet_date.strftime('%Y-%m-%d')
                                        meet_time_str=meet_time.strftime('%H:%M')
                                        result_data.append(
                                           {
                                            'order_id': search_all_orders_b[i][0],
                                            'username': search_usernames[0][1],
                                            'meet_type': meet_type,
                                            'meet_date': meet_date_str,
                                            'meet_time': meet_time_str,
                                           'real_name': search_usernames[0][2],
                                           'phone': search_usernames[0][7],
                                            'meet_location': search_all_orders_b[i][4],
                                            'meet_action':"送站"
                                               })
                                    else:
                                        return False,'接送形式编码有误'
                           else:
                               return False,'用户ID有误'
                 return True,result_data

        else:
            return False, '密码输入错误'
    else:
        return False, '不存在该服务人员'