def get_room_Imf(connecter):
    search_result = connecter.search('房型表', 'true')
    result_data=[]
    if len(search_result) > 0:
        for x in search_result:
            result_data.append({
                'room_id':x[0],
                'room_type':x[1],
                'room_price':x[2],
                '面积':x[4],
                '床':x[5],
                '每日打扫':x[6],
                '牙刷':x[7],
                '牙膏':x[8],
                '沐浴露':x[9],
                '洗发水':x[10],
                '免费wifi':x[11],
                '电视':x[12],
                '毛巾':x[13],
                '私人卫浴':x[14],
                '吹风机':x[15],
            })
        return True,result_data
    else:
        return False, '返回失败'
