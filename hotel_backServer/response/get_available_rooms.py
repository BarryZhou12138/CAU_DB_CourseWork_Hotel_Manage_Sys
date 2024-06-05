import DB.DB_control
import response.login
def get_available_rooms(username, password, room_id, connect:DB.DB_control.DB_connect):

    login_result,msg = response.login.login(username,password,'2',connect)
    if not login_result:
        return False,msg

    room = connect.direct_execute("select 房间号 from 房间表 where 房型号 = '%s' and 使用状态 = '空'"%(room_id))
    return True,room