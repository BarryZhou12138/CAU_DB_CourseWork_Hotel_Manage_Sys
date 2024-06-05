from nanoid import generate
import datetime 
import response.remove_order
import DB.DB_control

def update_order_by_user(username, password, order_id, check_in, check_out,new_room_type, connecter):
    print("update_order_by_user "+username+" "+password+" "+order_id+" "+check_in+" "+check_out+" "+new_room_type)
    search_result = connecter.search('用户表', "用户名='%s'"%username)
    if len(search_result)==1:
        if search_result[0][9]==password:
            search_new_room_type=connecter.search('房型表',"房型类别='%s'"%new_room_type)
            if len(search_new_room_type)==0:
                return False,'房型类型输入有误'
            return_information=add_new_order(username,password,new_room_type,check_in,check_out,connecter)
            print("add_new_order result:", return_information)
            if return_information[0]==True:
                new_order_id=return_information[1]
                search_new_order_id=connecter.search('订单表',"订单编号='%s'"%new_order_id)
                search_order_id=connecter.search('订单表',"订单编号='%s'"%order_id)
                if len(search_order_id)==0:
                    return False,'传入的订单有误'
                elif len(search_new_order_id)==0:
                    return False,'新订单生成失败'
                else:
                    connecter.update('订单表',"用户ID='%s',房型号='%s',证件号码='%s',预计入住日期='%s',预计离开日期='%s',预计住宿费用='%s',定金支付状态='%s'"%(search_new_order_id[0][1],search_new_order_id[0][2],search_new_order_id[0][3],search_new_order_id[0][4],search_new_order_id[0][5],search_new_order_id[0][6],search_new_order_id[0][7]),"订单编号='%s'"%order_id)
                    response.remove_order.remove_order(username, password, new_order_id,connecter)
                    return True,'更改接口成功'
            else:
                return False,'创建新订单失败'

        else:
            return False,'密码错误'
    else:
        return False,'用户还未注册或登录'

def add_new_order(username, password, room_type, check_in, check_out, connecter):
    print("add_new_order "+username+" "+password+" "+room_type+" "+check_in+" "+check_out)
    check_in_date = datetime.datetime.strptime(check_in[0:10],"%Y-%m-%d")
    check_out_date = datetime.datetime.strptime(check_out[0:10],"%Y-%m-%d")
    search_result = connecter.search('用户表', "用户名='%s'"%username)
    search_room_type = connecter.search('房型表',"房型类别='%s'"%room_type)
    if len(search_room_type)==0:
        return False,'房型类别输入有误'
    result_data=[]

    now_time = datetime.datetime.now()

        
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
                    return True,order_id
                else:
                    return False,'无剩余房间'
        else:
            return False,'密码错误'
    else:
        return False,'还未注册或登录'
