from nanoid import generate
import time 

def add_send_order(username, password, meet_id, meet_time,location,connecter):
    print("add_send_order "+username+" "+password+" "+meet_id+" "+meet_time+" "+location)
    search_result = connecter.search('用户表', "用户名='%s'"%username)
    search_order_id = connecter.search('订单表', "用户ID='%s' AND 预计入住日期 <= '%s' AND 预计离开日期 >= '%s'" % (
        search_result[0][0], meet_time, meet_time))
    n=len(search_order_id)

    if n == 0:
        return False, '请先在接送时间内订房再预定接送'
    
    search_meet_result = connecter.search('接送类型表',"接送形式编码='%s'"%meet_id)
    price=search_meet_result[0][2]
    meet_type=search_meet_result[0][1]
    result_data=[]

    if len(search_result) == 1:
        if search_result[0][9] == password:
            if n>= 1:
                 meet_order_id=generate(size=12)
                 connecter.insert('送站预约表(送站订单编号,接送形式编码,订单编号,送站日期,送站地址)',"('%s','%s','%s','%s','%s')"%(meet_order_id,meet_id,search_order_id[n-1][0],meet_time,location))
                 result_data.append(
                    {
                        'order_id':search_order_id[n-1][0],
                        'username':username,
                        'meet_id':meet_id,
                        'meet_time':meet_time,
                        'location':location,
                        'meet_type':meet_type,
                        'meet_price':price
                    }
                    )
                 return True, result_data
            else:
                return False,'还未下单'
        else:
            return False,'密码错误'
    else:
        return False,'还未注册或登录'
    


