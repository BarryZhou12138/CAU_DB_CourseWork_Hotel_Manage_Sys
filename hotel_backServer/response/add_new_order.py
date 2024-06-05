from nanoid import generate
import datetime 

def add_new_order(username, password, room_type, check_in, check_out, connecter):
    print("add_new_order "+username+" "+password+" "+room_type+" "+check_in+" "+check_out)
    check_in_date = datetime.datetime.strptime(check_in[0:10],"%Y-%m-%d")
    check_out_date = datetime.datetime.strptime(check_out[0:10],"%Y-%m-%d")
    search_result = connecter.search('用户表', "用户名='%s'"%username)
    search_room_type = connecter.search('房型表',"房型类别='%s'"%room_type)
    result_data=[]

    today_date = datetime.date.today()
    now_time = datetime.datetime(today_date.year, today_date.month, today_date.day)

    if len(connecter.search('订单表',"用户ID='%s' and ((预计入住日期>='%s' and 预计离开日期<='%s')or(预计入住日期>='%s' and 预计入住日期<='%s')or(预计离开日期<='%s' and 预计离开日期>='%s'))"%(search_result[0][0],check_in,check_out,check_in,check_out,check_out,check_in)))>=1:
        return False,'订单日期冲突'
        
    if len(search_result) == 1:
        if search_result[0][9] == password:
            if (check_out_date-check_in_date).days<=0 or (check_out_date-check_in_date).days>30 or (check_in_date-now_time).days<0:
                return False, '信息填入有误'
            else:
                certificate_id=search_result[0][3]
                user_id=search_result[0][0]
                order_id=generate(size=12)
                room_type = search_room_type[0][0]
                deposit = (check_out_date-check_in_date).days*int(search_room_type[0][3])
                connecter.direct_execute("call add_order('%s','%s','%s','%s','%s','%s')"%(order_id,user_id,room_type,certificate_id,check_in,check_out))
                connecter.commit()
                if len(connecter.search('订单表', "订单编号='%s'"%(order_id))) == 1:
                    result_data.append(
                    {
                        'order_id':order_id,
                        'username':username,
                        'room_type':room_type,
                        'certificate_id':certificate_id,
                        'check_in':check_in,
                        'check_out':check_out,
                        'deposit':deposit,
                    }
                    )
                    return True,result_data
                else:
                    return False,'无剩余房间'
        else:
            return False,'密码错误'
    else:
        return False,'还未注册或登录'


