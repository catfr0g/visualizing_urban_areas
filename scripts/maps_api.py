import requests
a = [55.74802022425328, 48.7462753296416]  # Latitude, Longtitude (rightclick+copy from googlemaps)
a=a[::-1] #longtitude, latitude
b = [a[0] + 0.03, a[1] + 0.02] #area of search

body = {"request":"pois","geometry":{"bbox":[a,b],"geojson":{"type":"Point","coordinates":a},"buffer":200}}
key='5b3ce3597851110001cf6248820c935b13e140fb9bff5b0bc86f678d'

headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    'Authorization': key,
    'Content-Type': 'application/json; charset=utf-8'
}
call = requests.post('https://api.openrouteservice.org/pois', json=body, headers=headers)
print(call.status_code, call.reason)
call=call.json()

info_nearby=[]
for item in call['features']:
    name=None
    categories=None
    try:
        name=item['properties']['osm_tags']['name']
        categories=item['properties']['category_ids']
        info_nearby.append((name,categories))
    except KeyError:
        pass
    
print(info_nearby)
# print(call.text)

# git remote add upstream <original-repository-url>
# git fetch upstream
# git checkout main
# git merge upstream/main
# git push origin main