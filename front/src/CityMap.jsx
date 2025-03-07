// src/CityMap.jsx
import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, GeoJSON, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';

import 'leaflet/dist/leaflet.css';

// Fix default icon issues in Leaflet + Webpack
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl:
    'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl:
    'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png'
});

function CityMap({ cityData }) {
  // Store the map instance once it's created
  const [map, setMap] = useState(null);

  // Style function for polygons
  const styleDistricts = (feature) => {
    const districtType = feature.properties.type;
    let fillColor = '#ccc';
    if (districtType === 'residential') fillColor = '#a1d99b';
    if (districtType === 'commercial') fillColor = '#fc9272';
    if (districtType === 'mixed') fillColor = '#9ecae1';

    return {
      color: '#333',
      weight: 1,
      fillColor,
      fillOpacity: 0.6
    };
  };

  // Attach popups to each polygon
  const onEachDistrict = (feature, layer) => {
    const districtName = feature.properties.name || 'Unnamed District';
    layer.bindPopup(`<strong>${districtName}</strong>`);
  };

  // Re-center the map whenever cityData changes
  useEffect(() => {
    if (map) {
      // Option 1: Instantly jump to location
      // map.setView(cityData.center, 13);

      // Option 2: Smooth transition
      map.flyTo(cityData.center, 13, {
        duration: 1.5 // seconds
      });
    }
  }, [map, cityData]);

  return (
    <MapContainer
      center={cityData.center} // initial center
      zoom={13}               // initial zoom
      style={{ width: '800px', height: '600px' }}
      whenCreated={setMap}    // store reference to map when ready
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
      />

      {/* District Polygons */}
      <GeoJSON
        data={cityData.geojson}
        style={styleDistricts}
        onEachFeature={onEachDistrict}
      />

      {/* Airbnb Markers */}
      {cityData.markers.map((marker) => (
        <Marker key={marker.id} position={[marker.lat, marker.lng]}>
          <Popup>{marker.title}</Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}

export default CityMap;
