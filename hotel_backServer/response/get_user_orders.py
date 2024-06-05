import datetime
import json

def get_user_orders(username, password,connecter):
    print("get_user_orders " + username + " " + password )
    search_result = connecter.search('用户表', "用户名='%s'" % username)
    result_data=[]
    if len(search_result)==1:
        if search_result[0][9] == password:
             search_room_order= connecter.search('订单表', "用户ID='%s'" % search_result[0][0])

             n=len(search_room_order)
             if n==0:
               return False,'还未创建订单'
             
             for j in range(0,n):
               room_order_id=search_room_order[j][0]
               search_room_type= connecter.search('房型表', "房型号='%s'" % search_room_order[j][2])
               result_data.append({
                'room_order_id':room_order_id,
                'order_type':"房间订单",
                'room_id':search_room_order[j][2],
                'room_type':search_room_type[0][1],
                'room_intro':search_room_type[0][16],
                'check_in': search_room_order[j][4].strftime('%Y-%m-%d'),
                'check_out': search_room_order[j][5].strftime('%Y-%m-%d'),
                'deposit':search_room_order[j][6],
                '支付状态':search_room_order[j][7],
            })
    
               search_food_id=connecter.search('点餐表', "订单编号='%s'" % room_order_id)
               m=len(search_food_id)
               if m>=1:
                for i in range(0,m):
                 search_dish_name=connecter.search('餐单表',"套餐编号='%s'"%search_food_id[i][2])
                 result_data.append({
                'food_order_id':search_food_id[i][0],
                'order_type':"食品订单",
                'dish_id': search_dish_name[0][0],
                'dish_name':search_dish_name[0][2],
                'dish_intro':search_dish_name[0][5],
                'dish_type': search_dish_name[0][1],
                'quantity':search_food_id[i][5],
                'order_time':str(search_food_id[i][4]),
                'total_price':search_food_id[i][6]
            })
            
    
               search_meet_id=connecter.search('接站预约表', "订单编号='%s'" % room_order_id)
               if len(search_meet_id)>=1:

                  for i in range(len(search_meet_id)):
                      search_meet_name = connecter.search('接送类型表', "接送形式编码='%s'" % search_meet_id[i][1])
                      result_data.append({
                    'meet_order_id':search_meet_id[i][0],
                    'order_type':"接站订单",
                    'meet_id':search_meet_name[0][0],
                    'meet_type':search_meet_name[0][1],
                    'meet_time': str(search_meet_id[i][3]),
                    'location':search_meet_id[i][4],
                    'meet_price':search_meet_name[0][2]
                })
            
    
               search_send_id=connecter.search('送站预约表', "订单编号='%s'" % room_order_id)
               if len(search_send_id)>=1:


                 for i in range(0,len(search_send_id)):
                    search_send_name = connecter.search('接送类型表', "接送形式编码='%s'" % search_send_id[0][1])
                    result_data.append({
                    'meet_order_id':search_send_id[i][0],
                    'order_type':"送站订单",
                    'meet_id':search_send_name[0][0],
                    'meet_type':search_send_name[0][1],
                    'meet_time':str(search_send_id[i][3]),
                    'location':search_send_id[i][4],
                    'meet_price':search_send_name[0][2]
                    })

             return True, json.dumps(result_data)
        
        else:
            return False, '密码错误'
    else:
        return False, '还未注册或登录'