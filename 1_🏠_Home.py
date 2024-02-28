import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.set_page_config(
    layout="wide",
    page_title="MY Transport",
    page_icon="🇲🇾"
)

# Customize page title
st.title("MY Transport")

st.markdown(
    """
    Your all in one unified platform to view real time publis transport status
    """
)



data = pd.DataFrame({
    'awesome cities' : ['Chicago', 'Minneapolis', 'Louisville', 'Topeka'],
    'lat' : [41.868171, 44.979840,  38.257972, 39.030575],
    'lon' : [-87.667458, -93.272474, -85.765187,  -95.702548]
})

st.map(data, size=70,)

# Adding code so we can have map default to the center of the data
# midpoint = (np.average(data['lat']), np.average(data['lon']))

# st.pydeck_chart(pdk.Deck(
#             map_style='mapbox://styles/mapbox/light-v9',
#                 initial_view_state=pdk.ViewState(
#                     mapboxApiAccessToken=st.secrets["mapboxtoken"],
#                     longitude=midpoint[0],
#                     latitude=midpoint[1],
#                     zoom=2,
#                     min_zoom=1,
#                     max_zoom=5,
#                     pitch=0
#                 ),
#             layers=[{
#                 'type': 'ScatterplotLayer',
#                 'data': data,
#                 'radiusScale': 250,
#    'radiusMinPixels': 5,
#                 'getFillColor': [248, 24, 148],
#             }]
#         ))