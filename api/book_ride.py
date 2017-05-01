"""
Lambda function to book a ride on our single tap App.
"""

def lambda_handler(event, context):
    import json
    import uuid
    from base64 import b64encode, b64decode
    import boto3
    import urllib
    import requests

    drop_details = {}
    result = {'statusCode': 400, 'body': json.dumps({'action_status': 'failure'})}
    body = json.loads(event.get('body', '{}'))
    
    # For user phone number verification
    enc_verification_code = body.get('enc_verification_code')
    verification_code = body.get('verification_code')
    if not enc_verification_code or not verification_code:
        return result

    # Using AWS KMS (Key management store), try to decrypt our encrypted verification code
    try:
        kms_client = boto3.client('kms')
        # Note that we've only one KMS stored that we could fetch plaintext directly,
        # If we'd multiple KMS configured, then we've to first parse the res and fetch plaintext
        # for our key only using its ARN
        res = kms_client.decrypt(CiphertextBlob=b64decode(enc_verification_code))['Plaintext']
    except Exception as e:
        return result

    # If unable to verify, return
    if res != verification_code:
        return result

    # Try to get product id
    p_id = body.get('p_id')
    if not p_id:
        return result

    # get pickup details and convert it to format that Careem API wants (i.e. serialization)
    pickup_details = {
        'longitude': body.get('p_lng', 0),
        'latitude': body.get('p_lat', 0),
        'nickname': 'UNI-VASTI'             # Static for now
    }

    # Similarly get drop off details and serialize it
    if body.get('d_lng') and body.get('d_lat'):
        drop_details = {
            'longitude': body.get('d_lng'),
            'latitude': body.get('d_lat'),
            'nickname': 'SADDAR'
        }

    # promo code, if any
    promo_code = body.get('promo_code', '')

    # Generate unique identifier for the customer
    uid = uuid.uuid4()
    
    # Static for NOW
    driver_notes = 'Ok'
    booking_type = 'NOW'
    phone_number = body.get('phone_number', '000000000')
    
    # Serialize customer details. Note that we are only getting phone number from 
    # our customers rest is static.
    customer_details = {
        'uuid': str(uid),
        'name': 'Anon',
        'email': 'anon@anon.com',
        'phone_number': phone_number
    }

    surge_id = body.get('surge_confirmation_id', '')

    # Finally, create payload for Careem API
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

    headers = {'Authorization': AUTH_TOKEN, 'Content-Type': 'application/json'}
    url = '{}/v1/bookings'.format(API_URL)
    try:
        response = requests.post(url=url, headers=headers, data=json.dumps(payload))
    except Exception:
        return result

    # Booking created successfully, Fetch booking details for SMS body
    booking_id = json.loads(response.content)['booking_id']
    url = '{0}/v1/bookings/{1}'.format(API_URL, booking_id)
    booking_details = requests.get(url=url, headers=headers, data=json.dumps(payload))
    booking_details = json.loads(booking_details.content)
    driver_details = booking_details.get('driver_details', {})
    if not driver_details: driver_details = {}
    vehicle_details = booking_details.get('vehicle_details', {})
    if not vehicle_details: vehicle_details = {}

    # Create SMS body
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
    url = "https://api.twilio.com/2010-04-01/Accounts/{0}/Messages.json".format(TWILIO_KEY_ID)
    data = {"To": phone_number, "From": TWILIO_NUMBER, "Body": message_text}
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

    return {'statusCode': 200, 'body': json.dumps({'action_status': 'success'})}
