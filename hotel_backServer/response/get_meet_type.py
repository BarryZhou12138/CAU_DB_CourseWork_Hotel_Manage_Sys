def get_meet_type(connecter):
    search_result = connecter.search('接送类型表', 'true')
    result_data=[]
    if len(search_result) > 0:
        for x in search_result:
            result_data.append(
                {
                    'meet_id':x[0],
                    'meet_type':x[1],
                    'meet_price':x[2],
                    'meet_intro':x[3]
                }
            )
        return True,result_data
    else:
        return False, '返回失败'