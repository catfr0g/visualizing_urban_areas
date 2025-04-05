import requests

# Define the Overpass API endpoint
overpass_url = "http://overpass-api.de/api/interpreter"

# Define the query to get POIs in a specific area (bounding box)
# This example gets all cafes within a bounding box around a specific location
overpass_query = """
[out:json];
node["amenity"="cafe"](50.6,7.0,50.7,7.3);
out body;
>;
out skel qt;
"""

# Send the request to the Overpass API
response = requests.get(overpass_url, params={'data': overpass_query})

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    # Process the data to extract POIs
    for element in data['elements']:
        if element['type'] == 'node':
            lat = element['lat']
            lon = element['lon']
            name = element['tags'].get('name', 'Unnamed')
            print(f"Name: {name}, Latitude: {lat}, Longitude: {lon}")
else:
    print(f"Error: {response.status_code}")