import datetime
def check_in(username,password,order_id,room_id,id_number,name,check_in_date, deposit,expected_check_out_date,connecter):
    print("check_in "+username+" "+password+" "+order_id+" "+room_id+" "+id_number+" "+name+" "+check_in_date+" "+deposit+" "+expected_check_out_date)
    search_result = connecter.search('服务人员表', "服务人员联系电话='%s'"%username)
    today_date = datetime.date.today()
    now_data = datetime.datetime(today_date.year,today_date.month,today_date.day)

    if len(search_result) == 1:
      if search_result[0][3] == password:
         search_order_id=connecter.search('订单表',"订单编号='%s'"%order_id)
         if search_order_id[0][3] != id_number:
            return False,'身份证号错误'
         if (now_data-datetime.datetime.strptime(expected_check_out_date[0:10], "%Y-%m-%d")).days>=0:
            return False,'入住日期错误'
         if len(search_order_id)==0:
            return False,'订单编号有误'
         search_rooms=connecter.search('房型表',"房型号='%s'"%search_order_id[0][2])
         if len(search_rooms)==0:
            return False,'房型号有误'
         search_room=connecter.search('房间表',"房型号='%s'"%search_order_id[0][2])
         n=len(search_room)
         search_status=0
         if n==0:
            return False,'房型号有误'
         for i in range(0,n):
            if search_room[i][2]=='满':
               search_status=search_status+1
         remaining_rooms=search_rooms[0][3]-search_status
         search_room_status=connecter.search('房间表',"房间号='%s'"%room_id)
         if remaining_rooms>0:
           if len(search_room_status)==0:
              return False,'房间号输入有误'
           else:
             if search_room_status[0][2]=='空':
               connecter.insert('入住登记表(订单编号,服务人员编号,房间号,证件号码,姓名,入住日期,押金,预计离开日期)',"('%s','%s','%s','%s','%s','%s','%s','%s')" % (order_id,search_result[0][0] , room_id, id_number,name, check_in_date, deposit, expected_check_out_date))
               connecter.update('房间表',"使用状态='满'","房间号='%s'"%room_id)
               return True,'入住登记成功'
             else:
                return False,'房间已被使用'
         else:
            return False,'没有剩余房间'
      else:
         return False,'服务人员密码错误'
    else:
      return False,'服务人员姓名输入错误'
