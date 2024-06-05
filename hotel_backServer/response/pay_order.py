def pay_order(username, password, order_id,connecter):
    print("pay_order "+username+" "+password+" "+order_id)
    search_result = connecter.search('用户表', "用户名='%s'"%username)
    search_order_id=connecter.search('订单表',"订单编号='%s'"%order_id)
    state='已支付'
    if len(search_result) == 1:
      if search_result[0][9] == password:
         if len(search_order_id)==1:
              if search_order_id[0][1]== search_result[0][0]:
                     connecter.update('订单表',"定金支付状态='%s'"%state,"订单编号='%s'"%order_id)
                     return True,'支付成功'
              else:
                  return False,'订单编号输入错误'
           
         else:
            return False, '订单不存在'
      else:
         return False,'密码错误'
    else:
      return False,'查无此人'

