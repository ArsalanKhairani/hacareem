def lambda_handler(event, context):
    import json
    import requests
    import urlparse
    import urllib

    query = urlparse.parse_qs(urlparse.urlsplit('?{}'.format(event['body'])).query)
    response = {'statusCode': 400, 'body': ''}
    body = query['Body']
    number = query['From']

    try:
        action, booking_id = body[0].split(' ')
    except:
        response['body'] = json.dumps({'error': 'Invalid message body'})
        return response

    if action.lower() not in ['c']:
        response['body'] = json.dumps({'error': 'Unsuported Action'})
        return response

    url = 'http://qa-interface.careem-engineering.com/v1/bookings/{}'.format(booking_id)
    headers = {'Authorization': 'test-crl54u6cj8f3a7hkc304359lhg', 'Content-Type': 'application/json'}

    try:
        res = requests.delete(url, headers=headers)
    except Exception:
        response['body'] = json.dumps({'error': 'Unable to cancel ride'})
        return response

    if not res.ok:
        response['body'] = json.dumps({'error': json.loads(res.content).get("message")})
        return response

    code_str = "Your booking ({}) has been cancelled".format(booking_id)
    url = "https://api.twilio.com/2010-04-01/Accounts/AC7908ac6b94e3dd4cfc8c83eb76f260b4/Messages.json"
    data = {"To": number, "From": "+17609614981", "Body": code_str}
    payload = urllib.urlencode(data)
    headers = {
        'authorization': "Basic QUM3OTA4YWM2Yjk0ZTNkZDRjZmM4YzgzZWI3NmYyNjBiNDoyZGM1NTkwMGM5N2Y2Yzg5OGU5N2M0MmM2Zjc3Yjg2YQ==",
        'content-type': "application/x-www-form-urlencoded"
    }

    res = requests.request("POST", url, data=payload, headers=headers)
    response = {'status': 'failure'}
    if not res.ok:
        response['message'] = 'Unable to send message'
        return response

    return res
