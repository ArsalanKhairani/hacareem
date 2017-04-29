
def oak():
    event = {'lat': '123', 'lon':'123'}
    result = {'actions_status': 'faliure'}
    lat = event['lat']
    lon = event['lon']
    payload = {'start_latitude': lat, 'start_longitude': lon}
    headers = {'Authorization':'test-crl54u6cj8f3a7hkc304359lhg'}
    import requests

    try:
        response = requests.get(url='http://qa-interface.careem-engineering.com/v1/estimates/time', headers=headers, params=payload)
    except Exception as e:
        return result

    if response.status_code == 200:
        return response.content

    return result

if __name__ == '__main__':
    print oak()