from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import re
import base64
import urllib
import urllib.parse
from DB import DB_control
import traceback
import response.login
import response.sign_up
import response.get_room_Imf
import response.updata_user_Imf
import response.get_room_Imf
import response.add_new_order
import response.pay_order
import response.get_userInf_complete
import response.remove_order
import response.get_menu
import response.add_food_order
import response.add_meet_order
import response.add_send_order
import response.get_user_orders
import response.check_in
import response.check_out
import response.pay_all_amounts
import response.get_checkin_orders
import response.get_checkout_orders
import response.admin_db_operations
import response.get_available_rooms
import response.Complete_food_order
import response.Conplete_meet_order
import response.get_user_info_by_phone
import response.delete_order_by_staff
import response.update_checkout_time
import response.change_room
import response.update_order_by_user
import response.update_order_by_staff
import response.get_meet_orders
import response.get_food_orders

host = ('localhost', 8888)

DB_connect = DB_control.DB_connect('root', '1234', 3308)

class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):#get的回调函数

        path = self.path.split('?')
        print(path[0])

        #登录
        if path[0] == '/login':
            response_data = {'code':'0' ,'msg':'登陆失败'}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            try:
                parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]

                call_back_result, msg = response.login.login(parm[1],parm[3],parm[5],DB_connect)
                if call_back_result:
                    response_data['code'] = '1'
            except(Exception):
                self.wfile.write(json.dumps(response_data).encode())
                return
            response_data['msg'] = msg
            self.wfile.write(json.dumps(response_data).encode())
        
        #注册
        elif path[0] == '/signup':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code':'0','msg':'注册失败'}
            try:
                call_back_result, msg = response.sign_up.sign_up(parm[1], parm[3], DB_connect)

                if call_back_result:
                    response_data['code'] = '1'
                response_data['msg'] = msg
            except:
                self.wfile.write(json.dumps(response_data).encode())
                return
            self.wfile.write(json.dumps(response_data).encode())

        #返回房型信息
        elif path[0] == '/get_room_Imf':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code':'0','msg':'返回房型信息失败'}
            try:
                call_back_result, data = response.get_room_Imf.get_room_Imf(DB_connect)

                if call_back_result:
                    response_data['code'] = '1'
                    response_data['msg'] = '成功'
                    response_data['data'] = data
            except:
                self.wfile.write(json.dumps(response_data).encode())
                return
            self.wfile.write(json.dumps(response_data).encode())

        #更新用户表
        elif path[0] == '/updata_user_Imf':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code':'0','msg':'更新失败'}
            # try:
            call_back_result, msg = response.updata_user_Imf.updata_user_Imf(parm[1], parm[3], parm[5], parm[7],parm[9], parm[11],parm[13], parm[15],parm[17],DB_connect)
            if call_back_result:
                response_data['code'] = '1'
            response_data['msg'] = msg
            # except:
            #     self.wfile.write(json.dumps(response_data).encode())
            #     return
            self.wfile.write(json.dumps(response_data).encode())

        #返回接送形式信息
        elif path[0] == '/get_meet_type':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code':'0','msg':'返回接送类型信息失败'}
            try:
                call_back_result, data = response.get_meet_type.get_meet_type(DB_connect)
                if call_back_result:
                    response_data['code'] = '1'
                    response_data['msg'] = '成功'
                    response_data['data'] = data
            except:
                self.wfile.write(json.dumps(response_data).encode())
                return
            self.wfile.write(json.dumps(response_data).encode())
        
        #创建预约订单
        elif path[0] == '/add_new_order':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code':'0','msg':'创建订单失败'}
            try:
                call_back_result, data = response.add_new_order.add_new_order(parm[1],parm[3],parm[5],parm[7],parm[9],DB_connect)
                if call_back_result:
                    response_data['code'] = '1'
                    response_data['msg'] = '成功'
                    response_data['data'] = data
                else:
                    response_data['msg'] = data
            except:
                self.wfile.write(json.dumps(response_data).encode())
                return
            self.wfile.write(json.dumps(response_data).encode())

        #定金支付
        elif path[0] == '/pay_order':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code':'0','msg':'定金支付失败'}
            try:
                call_back_result, data = response.pay_order.pay_order(parm[1],parm[3],parm[5],DB_connect)
                if call_back_result:
                    response_data['code'] = '1'
                    response_data['msg'] = '成功'
                    response_data['data'] = data
            except:
                self.wfile.write(json.dumps(response_data).encode())
                return
            self.wfile.write(json.dumps(response_data).encode())
        
        #获取用户信息填写状态
        elif path[0] == '/get_userInf_complete':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code':'0','msg':'填写不完整'}
            try:
                call_back_result, data = response.get_userInf_complete.get_userInf_complete(parm[1],parm[3],DB_connect)
                if call_back_result:
                    response_data['code'] = '1'
                    response_data['msg'] = '成功'
                    response_data['data'] = data
            except:
                self.wfile.write(json.dumps(response_data).encode())
                return
            self.wfile.write(json.dumps(response_data).encode())

        #删除订单
        elif path[0] == '/remove_order':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code':'0','msg':'删除失败'}
            try:
                call_back_result, msg = response.remove_order.remove_order(parm[1],parm[3],parm[5],DB_connect)
                if call_back_result:
                    response_data['code'] = '1'
                    response_data['msg'] = '删除成功'
                else:
                    response_data['msg'] = msg

            except:
                self.wfile.write(json.dumps(response_data).encode())
                return
            self.wfile.write(json.dumps(response_data).encode())

        #返回房型介绍图片
        elif path[0] == '/get_room_picture':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            with open('./static/room_picture/%s.jpg'%(parm[1]), 'rb') as f:
                img_data = f.read()

            self.send_response(200)  # 返回响应码
            self.send_header('Content-type', 'image/png')  # 设置Content-type头
            self.send_header('Content-Transfer-Encoding', 'base64')  # 设置Content-Transfer-Encoding头
            self.end_headers()  # 结束头部信息的添加

            self.wfile.write(img_data)  # 发送编码后的图像数据
        
        #返回菜品信息
        elif path[0] == '/get_menu':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code':'0','msg':'返回菜品信息失败'}
            try:
                call_back_result, data = response.get_menu.get_menu(DB_connect)
                if call_back_result:
                    response_data['code'] = '1'
                    response_data['msg'] = '成功'
                    response_data['data'] = data
            except:
                self.wfile.write(json.dumps(response_data).encode())
                return
            self.wfile.write(json.dumps(response_data).encode())

        #返回菜品介绍图片
        elif path[0] == '/get_dish_picture':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            with open('./static/dish_picture/%s.jpg'%(parm[1]), 'rb') as f:
                img_data = f.read()

            self.send_response(200)  # 返回响应码
            self.send_header('Content-type', 'image/png')  # 设置Content-type头
            self.send_header('Content-Transfer-Encoding', 'base64')  # 设置Content-Transfer-Encoding头
            self.end_headers()  # 结束头部信息的添加

            self.wfile.write(img_data)  # 发送编码后的图像数据
        
        #创建食品订单
        elif path[0] == '/add_food_order':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code':'0','msg':'创建食品订单失败'}
            # try:
            call_back_result, data = response.add_food_order.add_food_order(parm[1],parm[3],parm[5],parm[7],parm[9],parm[11],DB_connect)
            if call_back_result:
                response_data['code'] = '1'
                response_data['msg'] = '成功'
                response_data['data'] = data
            else:
                response_data['msg'] = data
            # except:
            #    self.wfile.write(json.dumps(response_data).encode())
            #    return
            self.wfile.write(json.dumps(response_data).encode())
        
        # 创建接送订单
        elif path[0] == '/add_meet_order':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code':'0','msg':'创建接站订单失败'}
            try:
                call_back_result, data = response.add_meet_order.add_meet_order(parm[1],parm[3],parm[5],parm[7],parm[9],DB_connect)
                if call_back_result:
                    response_data['code'] = '1'
                    response_data['msg'] = '成功'
                    response_data['data'] = data
                else:
                    response_data['msg'] = data
            except:
                self.wfile.write(json.dumps(response_data).encode())
                return
            self.wfile.write(json.dumps(response_data).encode())

        # 创建送站订单
        elif path[0] == '/add_send_order':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code':'0','msg':'创建送站订单失败'}
            try:
                call_back_result, data = response.add_send_order.add_send_order(parm[1],parm[3],parm[5],parm[7],parm[9],DB_connect)
                if call_back_result:
                    response_data['code'] = '1'
                    response_data['msg'] = '成功'
                    response_data['data'] = data
                else:
                    response_data['msg'] = data
            except:
                self.wfile.write(json.dumps(response_data).encode())
                return
            self.wfile.write(json.dumps(response_data).encode())

        #管理员数据库操作
        elif path[0] == '/admin_db_operations':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            parm[5] = parm[5].replace('+',' ')
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code':'0','msg':'运行失败','data':''}
            try:
                call_back_result, data = response.admin_db_operations.admin_db_operations(parm[1],parm[3],parm[5],DB_connect)
                if call_back_result:
                    response_data['code'] = '1'
                    response_data['data'] = data
                    response_data['msg'] = '运行成功'
                else:
                    response_data['msg'] = data
            except Exception as e:
                response_data['msg'] = traceback.format_exc()
                self.wfile.write(json.dumps(response_data,indent=4).encode())
                return
            self.wfile.write(json.dumps(response_data,indent=4).encode())

        # 获取用户所有订单
        elif path[0] == '/get_user_orders':

            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code':'0','msg':'获取用户所有订单失败'}
            try:
                call_back_result, data = response.get_user_orders.get_user_orders(parm[1],parm[3],DB_connect)
                if call_back_result:
                    response_data['code'] = '1'
                    response_data['msg'] = '成功'
                    response_data['data'] = data
                else:
                    response_data['msg'] = data
            except:
              self.wfile.write(json.dumps(response_data).encode())
              return
            self.wfile.write(json.dumps(response_data).encode())
        
        # 入住登记
        elif path[0] == '/check_in':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code':'0','msg':'入住登记失败'}
            try:
                call_back_result, data = response.check_in.check_in(parm[1],parm[3],parm[5],parm[7],parm[9],parm[11],parm[13],parm[15],parm[17],DB_connect)
                if call_back_result:
                    response_data['code'] = '1'
                    response_data['msg'] = '入住成功'
                    response_data['data'] = data
                else:
                    response_data['msg'] = data
            except:
                self.wfile.write(json.dumps(response_data).encode())
                return
            self.wfile.write(json.dumps(response_data).encode())

       # 退房登记
        elif path[0] == '/check_out':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code':'0','msg':'退房登记失败'}
            # try:
            call_back_result, data = response.check_out.check_out(parm[1],parm[3],parm[5],parm[7],parm[9],parm[11],parm[1],DB_connect)
            if call_back_result:
                response_data['code'] = '1'
                response_data['msg'] = '成功'
                response_data['data'] = data
            else:
                response_data['msg'] = data
            # except:
            #   self.wfile.write(json.dumps(response_data).encode())
            #   return
            self.wfile.write(json.dumps(response_data).encode())

        #完成食品订单
        elif path[0] == '/Complete_food_order':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code': '0', 'msg': '完成食品订单失败'}
            try:
                call_back_result, msg = response.Complete_food_order.Complete_food_order(parm[1], parm[3], parm[5], DB_connect)
                response_data['msg'] = msg
                if call_back_result:
                    response_data['code'] = '1'
            except:
                self.wfile.write(json.dumps(response_data).encode())
                return
            self.wfile.write(json.dumps(response_data).encode())

        #完成接送订单
        elif path[0] == '/Complete_meet_order':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code': '0', 'msg': '完成接送订单失败'}
            try:
                call_back_result, msg = response.Conplete_meet_order.Complete_meet_order(parm[1], parm[3], parm[5], parm[7], DB_connect)
                response_data['msg'] = msg
                if call_back_result:
                    response_data['code'] = '1'
            except:
                self.wfile.write(json.dumps(response_data).encode())
                return
            self.wfile.write(json.dumps(response_data).encode())

        # 获取传入日期内需要入住的订单
        elif path[0] == '/get_checkin_orders':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code': '0', 'msg': '订单获取失败'}
            try:
                call_back_result, data = response.get_checkin_orders.get_checkin_orders(parm[1], parm[3], parm[5],
                                                                                        DB_connect)
                if call_back_result:
                    response_data['code'] = '1'
                    response_data['msg'] = '成功'
                    response_data['data'] = data
                else:
                    response_data['msg'] = data
            except:
                self.wfile.write(json.dumps(response_data).encode())
                return
            self.wfile.write(json.dumps(response_data).encode())

        # 获取传入日期内需要退房的订单
        elif path[0] == '/get_checkout_orders':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code': '0', 'msg': '订单获取失败'}
            try:
                call_back_result, data = response.get_checkout_orders.get_checkout_orders(parm[1], parm[3], parm[5],
                                                                                          DB_connect)
                if call_back_result:
                    response_data['code'] = '1'
                    response_data['msg'] = '成功'
                    response_data['data'] = data
                else:
                    response_data['msg'] = data
            except:
                self.wfile.write(json.dumps(response_data).encode())
                return
            self.wfile.write(json.dumps(response_data).encode())

        # 支付所有费用
        elif path[0] == '/pay_all_amounts':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code': '0', 'msg': '支付失败'}
            try:
                call_back_result, data = response.pay_all_amounts.pay_all_amounts(parm[1], parm[3], parm[5], DB_connect)
                if call_back_result:
                    response_data['code'] = '1'
                    response_data['msg'] = '成功'
                    response_data['data'] = data
                else:
                    response_data['msg'] = data
            except:
                self.wfile.write(json.dumps(response_data).encode())
                return
            self.wfile.write(json.dumps(response_data).encode())

        #获取指定房型的空余房间
        elif path[0] == '/get_available_rooms':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code': '0', 'msg': '获取失败'}
            try:
                call_back_result, msg = response.get_available_rooms.get_available_rooms(parm[1], parm[3], parm[5], DB_connect)
                response_data['msg'] = msg
                if call_back_result:
                    response_data['code'] = '1'
                    response_data['data'] = msg
                    response_data['msg'] = '成功获取'
                else:
                    response_data['msg'] = msg
            except:
                self.wfile.write(json.dumps(response_data).encode())
                return
            self.wfile.write(json.dumps(response_data).encode())

        #使用手机号获取用户信息
        elif path[0] == '/get_user_info_by_phone':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code': '0', 'msg': '获取失败'}
            try:
                call_back_result, msg = response.get_user_info_by_phone.get_user_info_by_phone(parm[1], parm[3], parm[5],
                                                                                         DB_connect)
                response_data['msg'] = msg
                if call_back_result:
                    response_data['code'] = '1'
                    response_data['data'] = msg
                    response_data['msg'] = '成功获取'
                else:
                    response_data['msg'] = msg
            except:
                self.wfile.write(json.dumps(response_data).encode())
                return
            self.wfile.write(json.dumps(response_data).encode())

        #服务员删除订单
        elif path[0] == '/delete_order_by_staff':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code': '0', 'msg': '删除失败'}
            try:
                call_back_result, msg = response.delete_order_by_staff.delete_order_by_staff(parm[1], parm[3],
                                                                                               parm[5],
                                                                                               DB_connect)
                response_data['msg'] = msg
                if call_back_result:
                    response_data['code'] = '1'
                    response_data['data'] = msg
                    response_data['msg'] = '成功删除'
                else:
                    response_data['msg'] = msg
            except:
                self.wfile.write(json.dumps(response_data).encode())
                return
            self.wfile.write(json.dumps(response_data).encode())

        # 服务员修改预计离开时间
        elif path[0] == '/update_checkout_time':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code': '0', 'msg': '修改失败'}
            try:
                call_back_result, msg = response.update_checkout_time.update_checkout_time(parm[1], parm[3],
                                                                                             parm[5],parm[7],
                                                                                             DB_connect)
                response_data['msg'] = msg
                if call_back_result:
                    response_data['code'] = '1'
                    response_data['data'] = msg
                    response_data['msg'] = '修改成功'
                else:
                    response_data['msg'] = msg
            except:
                self.wfile.write(json.dumps(response_data).encode())
                return
            self.wfile.write(json.dumps(response_data).encode())

        # 服务员换房
        elif path[0] == '/change_room':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code': '0', 'msg': '换房失败'}
            try:
                call_back_result, msg = response.change_room.change_room(parm[1], parm[3],parm[5], parm[7], DB_connect)
                response_data['msg'] = msg
                if call_back_result:
                    response_data['code'] = '1'
                    response_data['data'] = msg
                    response_data['msg'] = '换房成功'
                else:
                    response_data['msg'] = msg
            except:
                self.wfile.write(json.dumps(response_data).encode())
                return
            self.wfile.write(json.dumps(response_data).encode())
        
        # 给服务员使用的订单更改接口
        elif path[0] == '/update_order_by_staff':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code':'0','msg':'服务人员更改接口失败'}
            try:
               call_back_result, data = response.update_order_by_staff.update_order_by_staff(parm[1],parm[3],parm[5],parm[7],parm[9],parm[11],DB_connect)
               if call_back_result:
                    response_data['code'] = '1'
                    response_data['msg'] = '成功'
                    response_data['data'] = data
               else:
                    response_data['msg'] = data
            except:
               self.wfile.write(json.dumps(response_data).encode())
               return
            self.wfile.write(json.dumps(response_data).encode())

        # 给用户使用的订单更改接口
        elif path[0] == '/update_order_by_user':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code':'0','msg':'用户更改接口失败'}
            try:
               call_back_result, data = response.update_order_by_user.update_order_by_user(parm[1],parm[3],parm[5],parm[7],parm[9],parm[11],DB_connect)
               if call_back_result:
                    response_data['code'] = '1'
                    response_data['msg'] = '成功'
                    response_data['data'] = data
               else:
                    response_data['msg'] = data
            except:
               self.wfile.write(json.dumps(response_data).encode())
               return
            self.wfile.write(json.dumps(response_data).encode())


        # 获取传入日期内需要完成的餐品订单
        elif path[0] == '/get_food_orders':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code':'0','msg':'订单获取失败'}
            try:
               call_back_result, data = response.get_food_orders.get_food_orders(parm[1],parm[3],parm[5],DB_connect)
               if call_back_result:
                    response_data['code'] = '1'
                    response_data['msg'] = '成功'
                    response_data['data'] = data
               else:
                    response_data['msg'] = data
            except:
               self.wfile.write(json.dumps(response_data).encode())
               return
            self.wfile.write(json.dumps(response_data).encode())

        # 获取传入日期内需要完成的接送订单
        elif path[0] == '/get_meet_orders':
            parm = [urllib.parse.unquote(x) for x in re.split('=|&', path[1])]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'code':'0','msg':'订单获取失败'}
            try:
               call_back_result, data = response.get_meet_orders.get_meet_orders(parm[1],parm[3],parm[5],DB_connect)
               if call_back_result:
                    response_data['code'] = '1'
                    response_data['msg'] = '成功'
                    response_data['data'] = data
               else:
                    response_data['msg'] = data
            except:
               self.wfile.write(json.dumps(response_data).encode())
               return
            self.wfile.write(json.dumps(response_data).encode())


        else: self.send_response(404)
    
 
if __name__ == '__main__':
    #端口监听开始，监听创建于host
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()