from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
import pandas as pd
from requests import get

import requests
# from forcediphttpsadapter.adapters import ForcedIPHTTPSAdapter

import os
import json
import time
import random

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
    #    response = json.loads(get(api).text)
        # session = requests.Session()
        # session.mount(api, ForcedIPHTTPSAdapter(dest_ip='103.191.76.170')) # type the desired ip
        # response = session.get(api, verify=False)
        # print(response.text)
        response = get(api, headers={'Accept': 'application/json', 'Content-Type': 'application/json' },
            #            proxies={
            # 'https': 'https://60.54.141.38:3128'}
                    ).text
        return json.loads(response)
   except (requests.exceptions.ConnectionError, json.decoder.JSONDecodeError):
       ''
        # st.write("Local ISP restricted")

# KTM Tracking API
RAPID_STATUS_URL = "https://api.mtrec.name.my/api/servicestatus"
ACTIVE_TRAIN_URL = "https://api.mtrec.name.my/api/spottersstatus"

status_data = getAPI(RAPID_STATUS_URL)
active_data = getAPI(ACTIVE_TRAIN_URL)


if (status_data):
    status_df = pd.DataFrame(status_data["Data"]).astype(str)
    active_df = pd.DataFrame(active_data["Data"]).astype(str)
else:
    status_df = pd.DataFrame([
        ["SPL", "LRT Sri Petaling Line", "", "Normal Service"],
        ["AGL", "LRT Ampang Line", "", "Normal Service"],
        ["KJL", "LRT Kelana Jaya Line", "", "Normal Service"],
        ["MRL", "KL Monorail Line", "", "Normal Service"],
        ["KGL", "MRT Kajang Line", "", "Normal Service"],
        ["PYL", "MRT Putrajaya Line", "", "Normal Service"],
        ["ERL", "KLIA Ekspres / Transit", "", "Normal Service"]
    ], columns=[
        "LineID",
        "Line",
        "Remark",
        "Status"
    ])
    active_df = pd.DataFrame([
        ["Line", "KJL", "MRL", "PYL", "KGL", "AGSPL"],
        ["Decommissioned", "13", "15", "0", "7", "0"],
        ["Not Spotted", "25", "7", "8", "15", "12"],
        ["In Service", "59", "2", "41", "36", "38"]
    ], columns=[
        "Kelana Jaya",
        "Monorail",
        "Putrajaya",
        "Kajang",
        "Ampang / Sri Petaling"
    ])


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
