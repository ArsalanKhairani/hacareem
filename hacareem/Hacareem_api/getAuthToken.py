def lambda_handler(event, context):
    import boto3
    from uuid import uuid4
    from base64 import b64encode
    import requests
    import json
    import urllib

    req_body = json.loads(event['body'])
    number = req_body.get('number')
    code = str(uuid4().fields[-1])[:6]
    code_str = "Your verification code is: {}".format(code)

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

    kms_client = boto3.client('kms')
    res = kms_client.encrypt(
        KeyId='arn:aws:kms:us-east-1:256503761977:key/8d484ab7-5c89-4ed0-a0ff-4fd076076cac',
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
