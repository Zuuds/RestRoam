from flask import Flask, jsonify, request
import requests
import json, xmltodict

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

app_id = ""
hash_token = ""


# to query, call: http://localhost:8000/gettoken
@app.route('/gettoken', methods=['GET'])
def get_token():
    # Set up URL to query

    app_id = "eb8lmx7x2e"
    hash_token = "ZWI4bG14N3gyZXx5Q0dmQTZ6UjNoNlJONTI0eTlnNE4zclRYcFAzMmYwcThRSkpNSUFI"
    url = f"https://api.iq.inrix.com/auth/v1/appToken?appId={app_id}&hashToken={hash_token}"

    response = requests.get(url)
    rjson = response.json()
    # Return token
    return rjson



@app.route('/getroute', methods=['GET'])
def findRoute():
    start = request.headers.get('start')
    dest = request.headers.get('dest')
    token = request.headers.get('Authorization')
    print(token)
    url = 'https://api.iq.inrix.com/findRoute'
    headers = {
    'accept': 'application/json',
    'Authorization': f'Bearer ${token}'
    }
    params = {
        'wp_1': start,
        'wp_2': dest,
        'routeOutputFields': 'P',
        'format': 'json',
    }

    response = requests.get(url, headers=headers, params=params)

    # Print the response or do further processing
    return response.json()



@app.route("/getpolygon", methods=['GET'])
def getPoly():
    token = request.headers.get('Authorization')
    url = 'https://api.iq.inrix.com/drivetimePolygons?center=37.770315%7C-122.446527&rangeType=A&duration=30'
    headers = {
    'accept': 'text/xml',
    'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # If the response is in XML format, you can access it using response.text
        xml_response = response.text
        # Process the XML response as needed
        # For example, you can convert it to JSON using xmltodict library
        # json_response = xmltodict.parse(xml_response)
        # return json_response

        # Alternatively, you can return the XML directly if that's what you need
        json_response = json.dumps(xmltodict.parse(xml_response), indent=2)
        return json_response, 200
    else:
        return {'error': 'Failed to fetch data'}, response.status_code

@app.route("/getnearbyinfo", methods=['GET'])
def getNearby():
    url = "https://travel-advisor.p.rapidapi.com/restaurants/list-by-latlng"
    lat,long = 37.766798,-122.433094
    max_val = 20
    querystring = {"latitude":f"{lat}","longitude":f"{long}","limit":f"{max_val}","currency":"USD","distance":"2","open_now":"false","lunit":"km","lang":"en_US"}

    headers = {
        "X-RapidAPI-Key": "e14abafa05msh523b478b2eb875ep1d959ejsn4aa6f50f385d",
        "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()['data']

    restaurants = []
    for place in data:
        # Check if 'name', 'latitude', and 'longitude' exist in the current place
        if 'name' in place and 'latitude' in place and 'longitude' in place and 'address' in place:
            name = place['name']
            latitude = place['latitude']
            longitude = place['longitude']
            address = place['address']
             
            restaurants.append({'Name': name, 'Latitude': latitude, 'Longitude': longitude, 'Address':address})

    return jsonify({'data':restaurants})

@app.route("/getparking", methods=['GET'])
def getParking():
    token = request.headers.get('Authorization')
    headers = {
    'accept': 'text/xml',
    'Authorization': f'Bearer {token}'
    }
    lat,long = 37.783335, -122.439405
    radius_meters = 200
    url = f'https://api.iq.inrix.com/lots/v3?point={lat}%7C{long}&radius={radius_meters}'

    response = requests.get(url,headers=headers)

    return response.json()

# Starting server using the run function
if __name__ == '__main__':
    port = 8000
    app.run(port=port)
    print(f"Server has been started at http://127.0.0.1:{port}/")
