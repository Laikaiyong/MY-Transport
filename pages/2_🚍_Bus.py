from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
from requests import get
import random
import time
import json

import streamlit as st

import folium
from streamlit_folium import st_folium

st.set_page_config(
    layout="wide",
    page_title="Bus | MY Transport",
    page_icon="🚍"
)

# if "load_state" not in st.session_state:
#      st.session_state.load_state = False

# @st.cache_data(experimental_allow_widgets=True)
# def filter_dataframe(df: pd.DataFrame, original_df: pd.DataFrame) -> pd.DataFrame:
#     """
#     Adds a UI on top of a dataframe to let viewers filter columns

#     Args:
#         df (pd.DataFrame): Original dataframe

#     Returns:
#         pd.DataFrame: Filtered dataframe
#     """
#     modify = st.checkbox("Add filters")

#     if not modify:
#         return original_df

#     df = df.copy()

#     modification_container = st.container()

#     with modification_container:
#         to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
#         for column in to_filter_columns:
#             left, right = st.columns((1, 20))
#             # Treat columns with < 10 unique values as categorical
#             if isinstance(df[column], pd.CategoricalDtype) or df[column].nunique() < 10:
#                 user_cat_input = right.multiselect(
#                     f"Values for {column}",
#                     df[column].unique(),
#                     default=list(df[column].unique()),
#                 )
#                 df = df[df[column].isin(user_cat_input)]
#             elif is_numeric_dtype(df[column]):
#                 _min = float(df[column].min())
#                 _max = float(df[column].max())
#                 step = (_max - _min) / 100
#                 user_num_input = right.slider(
#                     f"Values for {column}",
#                     min_value=_min,
#                     max_value=_max,
#                     value=(_min, _max),
#                     step=step,
#                 )
#                 df = df[df[column].between(*user_num_input)]
#             else:
#                 user_text_input = right.text_input(
#                     f"Substring or regex in {column}",
#                 )
#                 if user_text_input:
#                     df = df[df[column].astype(str).str.contains(user_text_input)]

#     return df


 
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

tab1, tab2 = st.tabs(["Map View", "Data Table View"])

with tab1:
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

with tab2:
    new_df = df.copy()
    st.dataframe(new_df)