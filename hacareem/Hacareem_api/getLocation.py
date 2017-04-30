def lambda_handler(event, context):
    import json
    GOOGLE_API_KEY = 'AIzaSyCe7ujESqCXdWnyHENEM-4RJiH_TjCeBTc'
    result = {'statusCode': 400, 'body': json.dumps({'action_status': 'failure'})}
    query = event.get('queryStringParameters', {}).get('query')
    if not query:
        return result

    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&key={}'.format(query, GOOGLE_API_KEY)
    import requests

    try:
        response = requests.get(url=url)
    except Exception as e:
        return result

    if response.status_code != 200:
        return result

    data = []
    for res in json.loads(getattr(response, 'text', '')).get('results', []):
        data.append({
            'place_name': res.get('formatted_address', ''),
            'lat': res.get('geometry', {}).get('location', {}).get('lat', 0),
            'lng': res.get('geometry', {}).get('location', {}).get('lng', 0)
        })

    result['statusCode'] = 200
    result['body'] = json.dumps(data)
    return result