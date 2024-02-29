from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
import pandas as pd
from requests import get

import streamlit as st

import folium
from streamlit_folium import st_folium

st.set_page_config(
    layout="wide",
    page_title="Bus | MY Transport",
    page_icon="🚍"
)
 
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

ip_address = [4.356413856735363, 103.00764593699655]
match option:
    case 'rapid-bus-kl':
        ip_address = [3.315143565060173, 101.60099765655472]

    case 'rapid-bus-kuantan': 
        ip_address = [3.8056856225280593, 103.3233851476217]
    
    case 'rapid-bus-penang':
        ip_address = [5.320985318929512, 100.36447204836247]
        
    case 'mybas-johor':
        ip_address =  [1.7958555965019127, 103.5584237529655]



m = folium.Map(
    ip_address, zoom_start=11
)

if option == 'mybas-johor':
    for index, row in df.iterrows():
        bus_pin = folium.CustomIcon(icon_image= "https://cdn-icons-png.flaticon.com/512/183/183756.png", icon_size=(30, 30))
        pdf = pd.DataFrame(
            data=[[
                "trip.tripId", row["trip.tripId"]], ["Latitude", row["position.latitude"]],
                ["Longitude", row["position.longitude"]
            ]], columns=[
                "Name",
                "Value"
            ]
        )
        html = row["trip.routeId"] + pdf.to_html(
            classes="table table-striped table-hover table-condensed table-responsive"
        )
        popup = folium.Popup(html)
        folium.Marker(
            [row["position.latitude"], row["position.longitude"]],
            icon=bus_pin,
            popup=popup, tooltip=row["trip.routeId"]
        ).add_to(m)
else:
    for index, row in df.iterrows():
        bus_pin = folium.CustomIcon(icon_image= "https://cdn-icons-png.flaticon.com/512/183/183756.png", icon_size=(30, 30))
        pdf = pd.DataFrame(
            data=[[
                "trip.tripId", row["trip.tripId"]],
                ["License Plate", row["vehicle.licensePlate"]],
                ["Speed", row["position.speed"]], ["Latitude", row["position.latitude"]],
                ["Longitude", row["position.longitude"]
            ]], columns=[
                "Name",
                "Value"
            ]
        )
        html = row["trip.routeId"] + pdf.to_html(
            classes="table table-striped table-hover table-condensed table-responsive"
        )
        popup = folium.Popup(html)
        folium.Marker(
            [row["position.latitude"], row["position.longitude"]],
            icon=bus_pin,
            popup=popup, tooltip=row["trip.routeId"]
        ).add_to(m)

st_folium(m, width=725, returned_objects=[])



# "https://rapid-track.vercel.app/api/track?route=173"