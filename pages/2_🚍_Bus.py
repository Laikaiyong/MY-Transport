from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
import pandas as pd
from requests import get

import streamlit as st

import folium
from streamlit_folium import st_folium
 
option = st.selectbox(
    'Bus options',
    ('rapid-bus-kl', 'rapid-bus-kuantan', 'rapid-bus-penang', 'mybas-johor'))
# Sample GTFS-R URL from Malaysia's Open API
URL = ""
if (option == "mybas-johor"):
    URL = "https://api.data.gov.my/gtfs-realtime/vehicle-position/mybas-johor"
else:
    URL = f'https://api.data.gov.my/gtfs-realtime/vehicle-position/prasarana?category={option}'
 
# Parse the GTFS Realtime feed
feed = gtfs_realtime_pb2.FeedMessage()
response = get(URL)
feed.ParseFromString(response.content)
 
# Extract and print vehicle position information
vehicle_positions = [MessageToDict(entity.vehicle) for entity in feed.entity]
print(f'Total vehicles: {len(vehicle_positions)}')
df = pd.json_normalize(vehicle_positions)
print(df)
# center on Liberty Bell, add marker
m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
folium.Marker(
    [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
).add_to(m)

if m:
    st_folium(m, width=725, returned_objects=[])
else:
    st.write("Map rendering")

"https://rapid-track.vercel.app/api/track?route=173"