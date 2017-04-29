def lambda_handler(event, context):
    import json
    result = {'statusCode': 400, 'body': json.dumps({'action_status': 'failure'})}
    lat = event.get('queryStringParameters', {}).get('lat', 0)
    lng = event.get('queryStringParameters', {}).get('lng', 0)
    payload = {'start_latitude': lat, 'start_longitude': lng}
    headers = {'Authorization': 'test-crl54u6cj8f3a7hkc304359lhg'}
    import requests

    try:
        response = requests.get(url='http://qa-interface.careem-engineering.com/v1/estimates/time', headers=headers,
                                params=payload)
    except Exception:
        return result

    if response.status_code != 200:
        return result

    return {'statusCode': 200, 'body': response.text}
