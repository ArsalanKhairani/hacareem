def lambda_handler(event, context):
    GOOGLE_API_KEY = 'AIzaSyCe7ujESqCXdWnyHENEM-4RJiH_TjCeBTc'
    result = {'actions_status': 'failure'}
    headers = {'Authorization': 'test-crl54u6cj8f3a7hkc304359lhg'}
    query = event.get('query', 'Gulshan')
    if not query:
        return result

    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&key={}'.format(query, GOOGLE_API_KEY)
    import requests
    import json
    try:
        response = requests.get(url=url, headers=headers)
    except Exception as e:
        return result

    if response.status_code != 200:
        return result

    result['actions_status'] = 'success'
    data = []
    for res in json.loads(getattr(response, 'text', '')).get('results', []):
        data.append({
            'place_name': res.get('formatted_address', ''),
            'lat': res.get('geometry', {}).get('location', {}).get('lat', 0),
            'lng': res.get('geometry', {}).get('location', {}).get('lng', 0)
        })

    result['data'] = data
    return result