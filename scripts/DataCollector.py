import requests

class DataCollector:
    def __init__(self):
        self.osm_mapping = {
            # AMENITY MAPPINGS
            'amenity': {
                # Nature
                'bbq': 'Nature', 'bench': 'Nature',
                # Ethnic
                'theatre': 'Ethnic', 'place_of_worship': 'Ethnic',
                # Tourist
                'cinema': 'Tourist', 'fountain': 'Tourist', 'stage': 'Tourist',
                'theater': 'Tourist', 'marketplace': 'Tourist', 'public_bath': 'Tourist',
                # Cafe street
                'cafe': 'Cafe street', 'fast_food': 'Cafe street', 'restaurant': 'Cafe street',
                # Nightlife
                'bar': 'Nightlife', 'biergarten': 'Nightlife', 'brothel': 'Nightlife',
                'casino': 'Nightlife', 'gambling': 'Nightlife', 'nightclub': 'Nightlife',
                'stripclub': 'Nightlife',
                # Elite r.e.
                'lounge': 'Elite r.e.',
                # Lower r.e.
                'prison': 'Lower r.e.', 'grave_yard': 'Lower r.e.'
            },
            
            # BUILDING MAPPINGS (handled differently as they need additional tag checks)
            'building': {
                # University
                'dormitory': 'University', 'college': 'University',
                'school': 'University', 'university': 'University',
                # Ethnic
                'religious': 'Ethnic', 'cathedral': 'Ethnic',
                'church': 'Ethnic', 'monastery': 'Ethnic',
                # Tourist
                'museum': 'Tourist', 'public': 'Tourist',
                'stadium': 'Tourist', 'grandstand': 'Tourist',
                'ship': 'Tourist', 'tower': 'Tourist',
                # Business center (handled in info_nearby_op)
                'office': 'Business center',
                # Elite r.e. (handled in info_nearby_op)
                'hotel': 'Elite r.e.',
                # Upper r.e. (handled in info_nearby_op)
                'apartments': 'Upper r.e.', 'commercial': 'Upper r.e.',
                'government': 'Upper r.e.',
                # Middle r.e. (handled in info_nearby_op)
                'residential': 'Middle r.e.', 'retail': 'Middle r.e.',
                'supermarket': 'Middle r.e.', 'civic': 'Middle r.e.',
                'parking': 'Middle r.e.', 'garages': 'Middle r.e.',
                # Lower r.e. (handled in info_nearby_op)
                'static_caravan': 'Lower r.e.', 'warehouse': 'Lower r.e.',
                'ruins': 'Lower r.e.',
                # cottage settlement
                'bungalow': 'cottage settlement', 'cabin': 'cottage settlement',
                'detached': 'cottage settlement', 'annexe': 'cottage settlement',
                'farm': 'cottage settlement', 'ger': 'cottage settlement',
                'house': 'cottage settlement', 'semidetached_house': 'cottage settlement',
                'terrace': 'cottage settlement'
            },
            
            # CLUB MAPPINGS
            'club': {
                # All tourist
                '*': 'Tourist'
            },
            
            # EDUCATION MAPPINGS
            'education': {
                # All university
                '*': 'University'
            },
            
            # HIGHWAY MAPPINGS
            'highway': {
                'living_street': 'Middle r.e.',
                'tertiary': 'cottage settlement',
                'residential': 'cottage settlement'
            },
            
            # LANDCOVER MAPPINGS
            'landcover': {
                # All nature
                '*': 'Nature'
            },
            
            # HISTORIC MAPPINGS
            'historic': {
                # All tourist
                '*': 'Tourist'
            },
            
            # LANDUSE MAPPINGS
            'landuse': {
                # All nature
                '*': 'Nature'
            },
            
            # LEISURE MAPPINGS
            'leisure': {
                'water_park': ['Nature', 'Tourist'],
                'stadium': ['Nature', 'Tourist'],
                'park': ['Nature', 'Tourist'],
                'picnic_table': ['Nature', 'Tourist'],
                'firepit': ['Nature', 'Tourist'],
                'beach_resort': ['Nature', 'Tourist'],
                'swimming_area': ['Nature', 'Tourist'],
                'outdoor_seating': 'Cafe street'
            },
            
            # MAN_MADE MAPPINGS
            'man_made': {
                'advertising': 'Tourist',
                'obelisk': 'Tourist',
                # All others are Lower r.e.
                '*': 'Lower r.e.'
            },
            
            # NATURAL MAPPINGS
            'natural': {
                # All nature
                '*': 'Nature'
            },
            
            # OFFICE MAPPINGS
            'office': {
                # All business center
                '*': 'Business center'
            },
            
            # SHOP MAPPINGS
            'shop': {
                # Downtown
                'boutique': 'Downtown', 'jewelry': 'Downtown',
                'leather': 'Downtown', 'shoes': 'Downtown',
                'watches': 'Downtown', 'perfumery': 'Downtown',
                # Cafe street
                'butcher': 'Cafe street', 'chocolate': 'Cafe street',
                'coffee': 'Cafe street', 'seafood': 'Cafe street',
                'alcohol': 'Cafe street',
                # Elite r.e.
                'boutique': 'Elite r.e.',
                # Upper r.e.
                'beauty': 'Upper r.e.', 'hairdresser': 'Upper r.e.',
                'massage': 'Upper r.e.',
                # Middle r.e.
                'bakery': 'Middle r.e.', 'convenience': 'Middle r.e.',
                'dairy': 'Middle r.e.', 'supermarket': 'Middle r.e.',
                'wholesale': 'Middle r.e.', 'mall': 'Middle r.e.',
                'chemist': 'Middle r.e.', 'doityourself': 'Middle r.e.',
                # Lower r.e.
                'second_hand': 'Lower r.e.', 'variety_store': 'Lower r.e.',
                'trade': 'Lower r.e.'
            },
            
            # TOURISM MAPPINGS
            'tourism': {
                'hotel': 'Upper r.e.',
                'hostel': 'Middle r.e.',
                'motel': 'Middle r.e.',
                # All others are Tourist
                '*': 'Tourist'
            },
            
            # WATERWAY MAPPINGS
            'waterway': {
                # All nature
                '*': 'Nature'
            }
        }
        
    def _get_mapped_category(self, osm_type, osm_value, tags=None):
        """Helper method to get the mapped category based on OSM type and value"""
        if osm_type not in self.osm_mapping:
            return None
            
        mapping = self.osm_mapping[osm_type]
        
        # Handle wildcard mappings
        if '*' in mapping and osm_value not in mapping:
            return mapping['*']
            
        # Handle specific value mappings
        if osm_value in mapping:
            return mapping[osm_value]
            
        # For building types that need additional tag checks
        if osm_type == 'building':
            if tags:
                # Check for Business center (office with specific material/height)
                if osm_value == 'office':
                    material = tags.get('building:material', '').lower()
                    height = float(tags.get('height', 0))
                    if material in ('glass', 'mirrored-glass') and height > 20:
                        return 'Business center'
                
                # Check for Elite r.e. (hotel or levels >20, specific material/height)
                if osm_value == 'hotel':
                    levels = int(tags.get('levels', 0))
                    material = tags.get('building:material', '').lower()
                    height = float(tags.get('height', 0))
                    if (levels > 20 or height > 60) and material in ('glass', 'mirrored-glass'):
                        return 'Elite r.e.'
                
                # Similar checks for other building types...
                
        return None

    def info_nearby_op(self, latitude, longitude, radius):
        """Use Overpass API to search for POIs within circle
           https://wiki.openstreetmap.org/wiki/Overture_categories"""
        overpass_url = "https://overpass-api.de/api/interpreter"

        overpass_query = f"""
        [out:json];
        (
            node["amenity"](around:{radius},{latitude},{longitude});
            node["shop"](around:{radius},{latitude},{longitude});
            node["tourism"](around:{radius},{latitude},{longitude});
            node["building"](around:{radius},{latitude},{longitude});
            node["club"](around:{radius},{latitude},{longitude});
            node["education"](around:{radius},{latitude},{longitude});
            node["highway"](around:{radius},{latitude},{longitude});
            node["landcover"](around:{radius},{latitude},{longitude});
            node["historic"](around:{radius},{latitude},{longitude});
            node["landuse"](around:{radius},{latitude},{longitude});
            node["leisure"](around:{radius},{latitude},{longitude});
            node["man_made"](around:{radius},{latitude},{longitude});
            node["natural"](around:{radius},{latitude},{longitude});
            node["office"](around:{radius},{latitude},{longitude});
            node["place"](around:{radius},{latitude},{longitude});
            node["public_transport"](around:{radius},{latitude},{longitude});
            node["waterway"](around:{radius},{latitude},{longitude});
            node["attraction"](around:{radius},{latitude},{longitude});
            node["playground"](around:{radius},{latitude},{longitude});
            node["healthcare"](around:{radius},{latitude},{longitude});
        );
        out body;
        >;
        out skel qt;
        """
        
        info_nearby = []
        try:
            response = requests.get(overpass_url, params={'data': overpass_query})
            if response.status_code == 200:
                data = response.json()
                for element in data['elements']:
                    if element['type'] == 'node':
                        tags = element.get('tags', {})
                        name = tags.get('name', 'Unnamed')
                        lat = element.get('lat')
                        lon = element.get('lon')
                        
                        mapped_categories = []
                        poi_type = None
                        
                        # Check all possible OSM tag types
                        for osm_type in self.osm_mapping.keys():
                            if osm_type in tags:
                                osm_value = tags[osm_type]
                                mapped = self._get_mapped_category(osm_type, osm_value, tags)
                                if mapped:
                                    if isinstance(mapped, list):
                                        mapped_categories.extend(mapped)
                                    else:
                                        mapped_categories.append(mapped)
                                poi_type = f"{osm_type}:{osm_value}"
                        
                        if mapped_categories:
                            info_nearby.append({
                                'name': name,
                                'coordinates': [lat, lon],
                                'categories': poi_type,
                                'custom': list(set(mapped_categories))  # Remove duplicates
                            })
            else:
                print(f"Error: {response.status_code}")
        except Exception as e:
            print(f"Error during Overpass query: {e}")
        
        return info_nearby
    
    def info_nearby_ors(self, latitude, longitude, step_lat, step_long):
        '''Use OpenRouteService to search for POI within rectangle. 

            Less POIs available rather than OP'''
        left_top_point = [latitude, longitude]  # Latitude, Longtitude (rightclick+copy from googlemaps)
        left_top_point=left_top_point[::-1] #longtitude, latitude
        right_bottom_point = [left_top_point[0] + step_long, left_top_point[1] + step_lat] #area of search
        
        body = {"request":"pois","geometry":{"bbox":[left_top_point,right_bottom_point],"geojson":{"type":"Point","coordinates":left_top_point},"buffer":200}}
        try:
            key=open('./secrets/ors_secret.txt').readline()
        except FileNotFoundError:
            print("Need to have './secrets/ors_secret.txt'\n \
                  Get key at https://account.heigit.org/signup")

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
            item['geometry']['coordinates']
            try:
                name=item['properties']['osm_tags']['name']
                coordinates=item['geometry']['coordinates']
                categories=item['properties']['category_ids']
                info_nearby.append({'name': name,
                                'coordinates': coordinates,
                                'categories': categories
                                })
            except KeyError:
                pass
        
        return info_nearby