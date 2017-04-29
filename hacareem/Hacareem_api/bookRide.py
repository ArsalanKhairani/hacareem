def lambda_handler(event, context):
    import json
    import uuid

    drop_details = {}
    result = {'statusCode': 400, 'body': json.dumps({'action_status': 'failure'})}
    #body = json.loads(event.get('body', '{}'))
    body = {
	"p_id": 1,
	"p_lng": 67.00994,
	"p_lat": 24.86146,
    "nickname": "IBA",
	"d_lng": 67.0398,
	"d_lat": 24.8744,
	"driver_notes": "Ajaa be",
	"booking_type": "NOW",
	"pickup_time": "1493456831",
	"promo_code": "",
	"phone_number": "0000-00000000",
	"surge_confirmation_id": ""
}
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
    #Static for NOW
    driver_notes = 'Ok'
    booking_type = 'NOW'
    customer_details = {
        'uuid': str(uid),
        'name': 'Anon',
        'email': 'anon@anon.com',
        'phone_number': body.get('phone_number', '000000000000')
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
        print response.text
    except Exception:
        return result

    if response.status_code != 200:
        return result

    return {'statusCode': 200, 'body': response.text}

if __name__ == '__main__':
    print lambda_handler({},{})