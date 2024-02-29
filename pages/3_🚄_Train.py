from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
import pandas as pd
from requests import get

import requests

import os
import json

import streamlit as st

import folium
from streamlit_folium import st_folium
 
st.set_page_config(
    layout="wide",
    page_title="Train | MY Transport",
    page_icon="🚄"
)
 
st.title("KTM Tracking")

# KTM Tracking API
KTM_URL = "https://api.data.gov.my/gtfs-realtime/vehicle-position/ktmb"
 
# Parse the GTFS Realtime feed
feed = gtfs_realtime_pb2.FeedMessage()
response = get(KTM_URL)
feed.ParseFromString(response.content)
 
# Extract and print vehicle position information
vehicle_positions = [MessageToDict(entity.vehicle) for entity in feed.entity]
print(f'Total vehicles: {len(vehicle_positions)}')
df = pd.json_normalize(vehicle_positions)

m = folium.Map(
    [4.356413856735363, 103.00764593699655], zoom_start=7
)


for index, row in df.iterrows():
    train_pin = folium.CustomIcon(icon_image= "https://cdn-icons-png.flaticon.com/512/1974/1974098.png", icon_size=(30, 30))
    pdf = pd.DataFrame(
        data=[[
            "trip.tripId", row["trip.tripId"]],
            ["ID", row["vehicle.id"]],
            ["Speed", row["position.speed"]], ["Latitude", row["position.latitude"]],
            ["Longitude", row["position.longitude"]
        ]], columns=[
            "Name",
            "Value"
        ]
    )
    html = row["vehicle.label"] + pdf.to_html(
        classes="table table-striped table-hover table-condensed table-responsive"
    )
    popup = folium.Popup(html)
    folium.Marker(
        [row["position.latitude"], row["position.longitude"]],
        icon=train_pin,
        popup=popup, tooltip=row["vehicle.label"]
    ).add_to(m)

st_folium(m, width=725, returned_objects=[])


# 2ND Section

st.title("Any other Trains")

tab1, tab2 = st.tabs(["Line Status", "Train Status"])


def getAPI(api) -> str:
   response = ""
   try:
       response = json.loads(get(api).text)
   except (requests.exceptions.ConnectionError, json.decoder.JSONDecodeError):
       time.sleep(2**30 + random.random()*0.01) #exponential backoff
       return getAPI(api)
   return response

# KTM Tracking API
RAPID_STATUS_URL = "https://api.mtrec.name.my/api/servicestatus"
ACTIVE_TRAIN_URL = "https://api.mtrec.name.my/api/spottersstatus"

status_data = getAPI(RAPID_STATUS_URL)
active_data = getAPI(ACTIVE_TRAIN_URL)


status_df = pd.DataFrame(status_data["Data"])
active_df = pd.DataFrame(active_data["Data"])


with tab1:
   st.dataframe(
        status_df,
        # column_config=[
        #     ""
        # ]
    )

with tab2:
    st.dataframe(
        active_df,
        # column_config=[
        #     ""
        # ]
    )
