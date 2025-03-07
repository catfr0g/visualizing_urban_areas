// App.jsx
import React, { useState, useEffect } from "react";
import {
  MapContainer,
  TileLayer,
  GeoJSON,
  Marker,
  Popup,
  useMap
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./App.css"; // <-- Our CSS from above

// Fix Leaflet icon paths
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png"
});

// Sample data
const citiesData = [
  {
    name: "New York",
    center: [40.7128, -74.006],
    geojson: {
      type: "FeatureCollection",
      features: [
        {
          type: "Feature",
          properties: { type: "residential", name: "District A" },
          geometry: {
            type: "Polygon",
            coordinates: [
              [
                [-74.01, 40.705],
                [-74.0, 40.705],
                [-74.0, 40.715],
                [-74.01, 40.715],
                [-74.01, 40.705]
              ]
            ]
          }
        },
        {
          type: "Feature",
          properties: { type: "commercial", name: "District B" },
          geometry: {
            type: "Polygon",
            coordinates: [
              [
                [-74.0, 40.705],
                [-73.99, 40.705],
                [-73.99, 40.715],
                [-74.0, 40.715],
                [-74.0, 40.705]
              ]
            ]
          }
        }
      ]
    },
    markers: [
      { id: 1, lat: 40.71, lng: -74.005, title: "AirBnB 1" },
      { id: 2, lat: 40.708, lng: -74.008, title: "AirBnB 2" }
    ]
  },
  {
    name: "San Francisco",
    center: [37.7749, -122.4194],
    geojson: {
      type: "FeatureCollection",
      features: [
        {
          type: "Feature",
          properties: { type: "residential", name: "District X" },
          geometry: {
            type: "Polygon",
            coordinates: [
              [
                [-122.425, 37.775],
                [-122.415, 37.775],
                [-122.415, 37.785],
                [-122.425, 37.785],
                [-122.425, 37.775]
              ]
            ]
          }
        },
        {
          type: "Feature",
          properties: { type: "mixed", name: "District Y" },
          geometry: {
            type: "Polygon",
            coordinates: [
              [
                [-122.415, 37.775],
                [-122.405, 37.775],
                [-122.405, 37.785],
                [-122.415, 37.785],
                [-122.415, 37.775]
              ]
            ]
          }
        }
      ]
    },
    markers: [
      { id: 3, lat: 37.78, lng: -122.42, title: "AirBnB A" },
      { id: 4, lat: 37.782, lng: -122.412, title: "AirBnB B" }
    ]
  }
];

// 1) FlyToCity: triggers smooth animation whenever center changes
function FlyToCity({ center }) {
  const map = useMap();
  useEffect(() => {
    map.flyTo(center, 13, { duration: 1.5 });
  }, [map, center]);
  return null;
}

// 2) Legend component
function Legend() {
  return (
    <div className="legend">
      <h2>Legend</h2>
      <div className="legend-item">
        <div className="color-box" style={{ backgroundColor: "#a1d99b" }} />
        <span>Residential</span>
      </div>
      <div className="legend-item">
        <div className="color-box" style={{ backgroundColor: "#fc9272" }} />
        <span>Commercial</span>
      </div>
      <div className="legend-item">
        <div className="color-box" style={{ backgroundColor: "#9ecae1" }} />
        <span>Mixed</span>
      </div>
      <div className="legend-item">
        <div className="color-box" style={{ backgroundColor: "#ccc" }} />
        <span>Other</span>
      </div>
    </div>
  );
}

// 3) Main App
export default function App() {
  const [selectedCity, setSelectedCity] = useState(citiesData[0]);

  // Style polygons
  const styleDistricts = (feature) => {
    const districtType = feature.properties.type;
    let fillColor = "#ccc";
    if (districtType === "residential") fillColor = "#a1d99b";
    if (districtType === "commercial") fillColor = "#fc9272";
    if (districtType === "mixed") fillColor = "#9ecae1";

    return {
      fillColor,
      color: "#333",
      weight: 1,
      fillOpacity: 0.6
    };
  };

  return (
    <div className="app-container">
      {/* LEFT PANEL */}
      <div className="left-panel">
        <h1>Interactive cities map</h1>

        <div className="city-selector">
          <label htmlFor="city-select">City:</label>
          <select
            id="city-select"
            value={selectedCity.name}
            onChange={(e) => {
              const city = citiesData.find((c) => c.name === e.target.value);
              setSelectedCity(city);
            }}
          >
            {citiesData.map((city) => (
              <option key={city.name} value={city.name}>
                {city.name}
              </option>
            ))}
          </select>
        </div>

        <Legend />
      </div>

      {/* RIGHT PANEL: MAP */}
      <div className="map-panel">
        <MapContainer
          center={selectedCity.center}
          zoom={13}
          className="leaflet-container"
        >
          <FlyToCity center={selectedCity.center} />

          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
          />

          <GeoJSON data={selectedCity.geojson} style={styleDistricts} />

          {selectedCity.markers.map((marker) => (
            <Marker key={marker.id} position={[marker.lat, marker.lng]}>
              <Popup>{marker.title}</Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}
