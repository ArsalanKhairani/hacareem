def lambda_handler(event, context):
    import json
    import uuid
    from base64 import b64encode, b64decode
    import boto3
    import urllib

    drop_details = {}
    result = {'statusCode': 400, 'body': json.dumps({'action_status': 'failure'})}
    body = json.loads(event.get('body', '{}'))
    print event
    print body
    enc_verification_code = body.get('enc_verification_code')
    verification_code = body.get('verification_code')
    print enc_verification_code
    print verification_code

    if not enc_verification_code or not verification_code:
        return result

    try:
        kms_client = boto3.client('kms')
        res = kms_client.decrypt(CiphertextBlob=b64decode(enc_verification_code))['Plaintext']
    except Exception as e:
        return result

    if res != verification_code:
        return result

    p_id = body.get('p_id')
    if not p_id:
        return result

    pickup_details = {
        'longitude': body.get('p_lng', 0),
        'latitude': body.get('p_lat', 0),
        'nickname': 'UNI-VASTI'
    }

    if body.get('d_lng') and body.get('d_lat'):
        drop_details = {
            'longitude': body.get('d_lng'),
            'latitude': body.get('d_lat'),
            'nickname': 'SADDAR'
        }

    promo_code = body.get('promo_code', '')

    uid = uuid.uuid4()
    # Static for NOW
    driver_notes = 'Ok'
    booking_type = 'NOW'
    phone_number = body.get('phone_number', '000000000')
    customer_details = {
        'uuid': str(uid),
        'name': 'Anon',
        'email': 'anon@anon.com',
        'phone_number': phone_number
    }

    surge_id = body.get('surge_confirmation_id', '')

    payload = {
        'product_id': p_id,
        'pickup_details': pickup_details,
        'driver_notes': driver_notes,
        'booking_type': booking_type,
        'customer_details': customer_details,
        'surge_conformation_id': surge_id,
        'pickup_time': '1493456831',
        'promo_code': promo_code,
        'dropoff_details': drop_details
    }

    headers = {'Authorization': 'test-crl54u6cj8f3a7hkc304359lhg', 'Content-Type': 'application/json'}
    import requests
    try:
        response = requests.post(url='http://qa-interface.careem-engineering.com/v1/bookings', headers=headers,
                                 data=json.dumps(payload))
    except Exception:
        return result

    # if not response.ok:
    #     return result

    # Booking created successfully
    booking_id = json.loads(response.content)['booking_id']
    booking_details = requests.get(url='http://qa-interface.careem-engineering.com/v1/bookings/{0}'.format(booking_id),
                                   headers=headers, data=json.dumps(payload))

    booking_details = json.loads(booking_details.content)
    driver_details = booking_details.get('driver_details', {})
    if not driver_details: driver_details = {}
    vehicle_details = booking_details.get('vehicle_details', {})
    if not vehicle_details: vehicle_details = {}

    driver_details_text = "Captain: {0}, Contact Number: {1}".format(driver_details.get('driver_name', 'Abdul Shakoor'),
                                                                     driver_details.get('driver_number', '0000-000000'))
    vehicle_details_text = "Vehicle: {0}-{1}, bearing number {2}".format(vehicle_details.get('make', 'Perfect'),
                                                                         vehicle_details.get('model', 'NEW'),
                                                                         vehicle_details.get('license_plate',
                                                                                             'WWW-404'))
    booking_details_text = "Status of Trip: {0}".format(booking_details.get('status').replace('_', ' ').title())
    booking_id_text = "Booking ID: {0}".format(booking_id)

    message_text = "\n".join([booking_details_text, vehicle_details_text, driver_details_text, booking_id_text])

    # Dispatch SMS to user after ride creation
    url = "https://api.twilio.com/2010-04-01/Accounts/AC7908ac6b94e3dd4cfc8c83eb76f260b4/Messages.json"
    data = {"To": phone_number, "From": "+17609614981", "Body": message_text}
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

    return {'statusCode': 200, 'body': json.dumps({'action_status': 'success'})}

