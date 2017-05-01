"""
Lambda function to get products of careem in our current location.
For static kiosk this API can be cached.
"""

def lambda_handler(event, context):
    import json
    import requests

    result = {'statusCode': 400, 'body': json.dumps({'action_status': 'failure'})}
    lat = event.get('queryStringParameters', {}).get('lat', 0)
    lng = event.get('queryStringParameters', {}).get('lng', 0)
    payload = {'latitude': lat, 'longitude': lng}
    headers = {'Authorization': AUTH_TOKEN}

    try:
        url = '{}/v1/products'.format(API_URL)
        response = requests.get(url=url, headers=headers, params=payload)
    except Exception:
        return result

    if response.status_code != 200:
        return result

    return {'statusCode': 200, 'body': response.text}
