"""
Incomplete.
"""

def lambda_handler(event, context):
    import json
    import requests

    result = {'statusCode': 400, 'body': json.dumps({'action_status': 'failure'})}
    s_lat = event.get('queryStringParameters', {}).get('s_lat', 0)
    s_lon = event.get('queryStringParameters', {}).get('s_lon', 0)
    e_lat = event.get('queryStringParameters', {}).get('e_lat', 0)
    e_lon = event.get('queryStringParameters', {}).get('e_lon', 0)
    # For now it is NOW
    b_type = event.get('queryStringParameters', {}).get('b_type', 'NOW')

    p_id = event.get('queryStringParameters', {}).get('p_id')

    if not p_id:
        return result

    payload = {
        'start_latitude': s_lat,
        'start_longitude': s_lon,
        'end_latitude': e_lat,
        'end_longitude': e_lon,
        'booking_type': b_type,
        'product_id': p_id
    }
    headers = {'Authorization': AUTH_TOKEN}

    try:
        url = '{}/v1/estimates/price'.format(API_URL)
        response = requests.get(url=url, headers=headers, params=payload)
    except Exception:
        return result

    if response and getattr(response, 'status_code', 0) != 200:
        return result

    return {'statusCode': 200, 'body': response.text}
