"""
Lambda function to generate auth token for a single request and send it via SMS to customer
"""

def lambda_handler(event, context):
    import boto3
    from uuid import uuid4
    from base64 import b64encode
    import requests
    import json
    import urllib

    # Fetch number from the request body
    req_body = json.loads(event['body'])
    number = req_body.get('number')

    # Generate Code. For one time code use python OTP (pyotp) package
    code = str(uuid4().fields[-1])[:6]
    code_str = "Your verification code is: {}".format(code)

    url = "https://api.twilio.com/2010-04-01/Accounts/{0}/Messages.json".format(TWILIO_KEY_ID)
    data = {"To": number, "From": TWILIO_NUMBER, "Body": code_str}
    payload = urllib.urlencode(data)
    headers = {
        'authorization': TWILIO_BASE64_AUTH,
        'content-type': "application/x-www-form-urlencoded"
    }

    # Send request to Twilio API to generate SMS
    res = requests.request("POST", url, data=payload, headers=headers)
    response = {'status': 'failure'}
    if not res.ok:
        response['message'] = 'Unable to send message'
        return response

    # Using AWS KMS encrypt the token and send it in response. Client will then send it back in the next request
    # That way we don't have to maintain any database on our side.
    kms_client = boto3.client('kms')
    res = kms_client.encrypt(
        KeyId=KMS_KEY_ARN,
        Plaintext=code
    )

    response = {'status': 'failure'}
    if res.get('ResponseMetadata').get('HTTPStatusCode', 0) != 200:
        response['message'] = 'Unable to encrypt key'
        return response

    enc_key = b64encode(res[u'CiphertextBlob'])
    response['status'] = 'success'
    response['message'] = {'enc_auth_token': enc_key}
    return {'statusCode': 200, 'body': json.dumps(response)}
