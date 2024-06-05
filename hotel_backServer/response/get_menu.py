def get_menu(connecter):
    search_result = connecter.search('餐单表', 'true')
    result_data=[]
    if len(search_result) > 0:
        for x in search_result:
            result_data.append(
                {
                    'dish_id':x[0],
                    'dish_type':x[1],
                    'dish_name':x[2],
                    'dish_price':x[3],
                    'dish_taste':x[4],
                    'date_intro':x[5]
                }
            )
        return True,result_data
    else:
        return False, '返回餐单失败'
