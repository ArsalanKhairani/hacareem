def lambda_handler(event, context):
    import json
    result = {'statusCode': 400, 'body': json.dumps({'action_status': 'failure'})}
    s_lat = event.get('s_lat', 0)
    s_lon = event.get('s_lon', 0)
    e_lat = event.get('e_lat', 0)
    e_lon = event.get('e_lon', 0)
    # For now it is NOW
    b_type = event.get('b_type', 'NOW')

    p_id = event.get('p_id', 0)
    
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
    except Exception:
        return result

    if response and getattr(response, 'status_code', 0) != 200:
        return result

    return {'statusCode': 200, 'body': response.text}