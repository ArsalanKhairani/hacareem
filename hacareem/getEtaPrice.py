
def oak():
    event = {'s_lat': '123', 's_lon':'123'}
    result = {'actions_status': 'faliure'}
    s_lat = event.get('s_lat', '')
    s_lon = event.get('s_lon', '')
    e_lat = event.get('e_lat', '')
    e_lon = event.get('e_lon', '')
    b_type = event.get('b_type', '')
    p_id = event.get('p_id', '')
    
    payload = {
        'start_latitude': s_lat,
        'start_longitude': s_lon,
        'end_latitude': e_lat,
        'end_longitude': e_lon,
        'booking_type': b_type,
        'product_id': p_id
    }
    headers = {'Authorization':'test-crl54u6cj8f3a7hkc304359lhg'}
    import requests

    try:
        response = requests.get(url='http://qa-interface.careem-engineering.com/v1/estimates/price', headers=headers, params=payload)
    except Exception as e:
        return result

    return response

if __name__ == '__main__':
    print oak().content