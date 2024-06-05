def updata_user_Imf(username,name,id_number,age,certificate_type,sex,phoneNumber,email,password,connecter):
    print("updata_user_Imf_callback "+username+" "+name+" "+id_number+" "+age+" "+certificate_type+" "+sex+" "+phoneNumber+" "+email+" "+password)
    search_result = connecter.search('用户表', "用户名='%s'"%username)
    if len(search_result) == 1:
      if search_result[0][9] == password:
          if int(age)>130 or int(age)<0 or len(phoneNumber) >20 or (sex!='男' and sex!='女') or (certificate_type!='身份证' and certificate_type!='港澳通行证' and certificate_type!='护照' and certificate_type!='外国人永久居留身份证') or (len(id_number)!=18 and len(id_number)!=9 and len(id_number)!=11):
              return False,'信息填入有误'
          else:
            # connecter.update('用户表(姓名，证件号码，年龄，证件类型，性别，联系电话，邮箱)',"('%s','%s','%d','%s','%s','%s','%s','%s')"%(name,id_number,age,certificate_type,sex,phoneNumber,email))
            connecter.update('用户表',"姓名='%s',证件号码='%s',年龄='%s',证件类型='%s',性别='%s',联系电话='%s',邮箱='%s'"%(name,id_number,age,certificate_type,sex,phoneNumber,email),"用户名='%s'"%username)
            return True,'更新成功'
      else:
         return False,'密码错误'
    else:
      return False,'查无此人'
