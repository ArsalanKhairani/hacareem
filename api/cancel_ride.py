"""
Lambda function to cancel a ride using SMS. Twilio needs to be configured to call Endpoint
attached to this lambda, whenever message is received.
"""

def lambda_handler(event, context):
    import json
    import requests
    import urlparse
    import urllib

    # Parse request body from Twilio.
    query = urlparse.parse_qs(urlparse.urlsplit('?{}'.format(event['body'])).query)
    response = {'statusCode': 400, 'body': ''}
    body = query['Body']
    number = query['From']

    # Get booking id and action from body
    try:
        action, booking_id = body[0].split(' ')
    except:
        response['body'] = json.dumps({'error': 'Invalid message body'})
        return response

    # If action is C (for cancel), then only proceed
    # This way we could build logic for other actions as well
    if action.lower() not in ['c']:
        response['body'] = json.dumps({'error': 'Unsuported Action'})
        return response

    # Call careem endpoint for delete
    url = '{}/v1/bookings/{}'.format(API_URL, booking_id)
    headers = {'Authorization': AUTH_TOKEN, 'Content-Type': 'application/json'}
    try:
        res = requests.delete(url, headers=headers)
    except Exception:
        response['body'] = json.dumps({'error': 'Unable to cancel ride'})
        return response

    if not res.ok:
        response['body'] = json.dumps({'error': json.loads(res.content).get("message")})
        return response

    # Form message body
    code_str = "Your booking ({}) has been canceled".format(booking_id)
    url = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json".format(TWILIO_KEY_ID)
    data = {"To": number, "From": TWILIO_NUMBER, "Body": code_str}
    payload = urllib.urlencode(data)
    headers = {
        'authorization': TWILIO_BASE64_AUTH,
        'content-type': "application/x-www-form-urlencoded"
    }

    res = requests.request("POST", url, data=payload, headers=headers)
    response = {'status': 'failure'}
    if not res.ok:
        response['message'] = 'Unable to send message'
        return response

    return res
