def lambda_handler(event, context):
    import json
    GOOGLE_API_KEY = 'AIzaSyCe7ujESqCXdWnyHENEM-4RJiH_TjCeBTc'
    result = {'statusCode': 400, 'body': json.dumps({'action_status': 'failure'})}
    headers = {}
    headers[
        'X-Amz-Security-Token'] = 'FQoDYXdzEGQaDGwPGLl7hg1EciWaUSK3A3OICFfBZPkuOUKH0aPp2eIaXKciU77UPaCYoxxrIGzKT5VRf7KZy277n4iKTiUpApAoiHcZZ/7S1tuy9Fxj1MnznEmBaOdFUbcyUaAH8JYNXUaZysYeqH7CAeNQ9Ys/u5V4v+AQHIU4uaiAFQH8BLrh8ph2BE8/+Nm4TDdX/CrqPDcNEISXoB3zgnIU0lbMsGL8FCVm03+dFgT5qzcijFHcB3O4v+C5F4Q5E2ekg7CYyirrpC+USKd0L9mk40H+p3ObxG3azFPk+yIrzCT3tajyyOCH0Ad0VmV7K2mx4Gj/z04N+ylkZfNEQWb2lQPLX9gsZ5'
    query = event.get('queryStringParameters', {}).get('query')
    if not query:
        return result

    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&key={}'.format(query, GOOGLE_API_KEY)
    import requests

    try:
        response = requests.get(url=url, headers=headers)
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