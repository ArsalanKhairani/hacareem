def lambda_handler(event, context):
    result = {'actions_status': 'failure'}
    lat = event.get('lat', 0)
    lon = event.get('lon', 0)
    payload = {'start_latitude': lat, 'start_longitude': lon}
    headers = {'Authorization':'test-crl54u6cj8f3a7hkc304359lhg'}
    import requests

    try:
        response = requests.get(url='http://qa-interface.careem-engineering.com/v1/estimates/time', headers=headers, params=payload)
    except Exception:
        return result

    if response and getattr(response, 'status_code', 0) != 200:
        return result

    return response
