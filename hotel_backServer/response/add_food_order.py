from nanoid import generate
import time

def add_food_order(username, password, dish_id, delivery_time, quantity, taste, connecter):
    print("add_food_order " + username + " " + password + " " + dish_id + " " + delivery_time + " " + quantity + " " + taste)
    search_result = connecter.search('用户表', "用户名='%s'" % username)
    search_order_id = connecter.search('订单表', "用户ID='%s' AND 预计入住日期 <= '%s' AND 预计离开日期 >= '%s'" % (
        search_result[0][0], delivery_time, delivery_time))
    n = len(search_order_id)

    if n == 0:
        return False, '请先订房入住再预定餐点'

    search_room_number = connecter.search('入住登记表', "订单编号='%s'" % (search_order_id[n - 1][0]))
    search_price = connecter.search('餐单表', "套餐编号='%s'" % dish_id)
    total_price = float(search_price[0][3]) * int(quantity)
    if len (search_room_number)==1:
        room_number = search_room_number[0][2]

    result_data = []

    delivery_time_date = time.strptime(delivery_time.replace('+','T'), "%Y-%m-%dT%H-%M-%S")
    now_time = time.localtime()

    if len(search_result) == 1:
        if search_result[0][9] == password:
            if n >= 1:
                if len(search_room_number) == 1:
                    diff_minutes = (time.mktime(delivery_time_date) - time.mktime(now_time)) // 60
                    if diff_minutes < 30:
                        return False, '送餐时间必须晚于当前时间30分钟'
                    elif diff_minutes > 3 * 24 * 60:
                        return False, '送餐时间不能超过3天'
                    else:
                        food_order_id = generate(size=12)
                        connecter.insert('点餐表(点餐单号,房间号,套餐编号,订单编号,送餐时间,就餐人数,点餐费用,套餐口味)',
                                         "('%s','%s','%s','%s','%s','%s','%s','%s')" % (
                                         food_order_id, room_number, dish_id, search_order_id[n - 1][0],
                                         delivery_time.replace('+',' '), quantity, total_price, taste))
                        result_data.append(
                            {
                                'order_id': search_order_id[n - 1][0],
                                'username': username,
                                'dish_id': dish_id,
                                'quantity': quantity,
                                'delivery_time': delivery_time,
                                'total_price': total_price,
                                'taste': taste
                            }
                        )
                        return True, result_data
                else:
                    return False, '还未入住'
            else:
                return False, '还未下单'
        else:
            return False, '密码错误'
    else:
        return False, '还未注册或登录'