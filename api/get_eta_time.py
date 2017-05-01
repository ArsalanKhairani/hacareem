"""
Lambda function to get estimated time of ride arrival using Careem's API.
"""

def lambda_handler(event, context):
    import json
    import requests
    
    result = {'statusCode': 400, 'body': json.dumps({'action_status': 'failure'})}
    lat = event.get('queryStringParameters', {}).get('lat', 0)
    lng = event.get('queryStringParameters', {}).get('lng', 0)
    payload = {'start_latitude': lat, 'start_longitude': lng}
    headers = {'Authorization': AUTH_TOKEN}

    try:
        response = requests.get(url='{}/v1/estimates/time'.format(API_URL), headers=headers, params=payload)
    except Exception:
        return result

    if response.status_code != 200:
        return result

    return {'statusCode': 200, 'body': response.text}
