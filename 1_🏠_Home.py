import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

from streamlit_folium import st_folium
import folium


def render_page():
    st.set_page_config(
        layout="wide",
        page_title="MY Transport",
        page_icon="🇲🇾"
    )

    # Customize page title
    st.title("MY Transport")

    st.markdown(
        """
        Your all in one unified platform to view real time public transport status
        """
    )

    st.info(
        "This is a unified platforms for Malaysia Public Transports Live Tracking (Dependent on Available APIs)"
    )
    
    st.title("Supporting (So far)")
    
    # Kuantan
    kuantan_pdf = pd.DataFrame(
        data=[["rapid-bus-kuantan", "Bus"]], columns=["Name", "Type"]
    )
    
    kuantan_html = "Kuantan\n" + kuantan_pdf.to_html(
        classes="table table-striped table-hover table-condensed table-responsive"
    )
    kuantan_popup = folium.Popup(kuantan_html)
    
    # KL
    kl_pdf = pd.DataFrame(
        data=[
            ["rapid-bus-kl", "Bus"],
            ["KTMB", "Train"],
            ["All Other Train", "Train"],
        ], columns=["Name", "Type"]
    )
    
    kl_html = "Kuala Lumpur\n" + kl_pdf.to_html(
        classes="table table-striped table-hover table-condensed table-responsive"
    )
    kl_popup = folium.Popup(kl_html)
    
    # Penang
    penang_pdf = pd.DataFrame(
        data=[["rapid-bus-penang", "Bus"]], columns=["Name", "Type"]
    )
    
    penang_html = "Penang\n" + penang_pdf.to_html(
        classes="table table-striped table-hover table-condensed table-responsive"
    )
    penang_popup = folium.Popup(penang_html)
    
    
    # johor
    johor_pdf = pd.DataFrame(
        data=[["mybas-johor", "Bus"]], columns=["Name", "Type"]
    )
    
    johor_html = "Johor\n" + johor_pdf.to_html(
        classes="table table-striped table-hover table-condensed table-responsive"
    )
    johor_popup = folium.Popup(johor_html)
    
    
    # Penang
    penang_pdf = pd.DataFrame(
        data=[["rapid-bus-penang", "Bus"]], columns=["Name", "Type"]
    )
    
    penang_html = "Penang\n" + penang_pdf.to_html(
        classes="table table-striped table-hover table-condensed table-responsive"
    )
    penang_popup = folium.Popup(penang_html)

    m = folium.Map(
        [4.356413856735363, 103.00764593699655], zoom_start=7
    )
    
    
    folium.Marker(
        [3.8056856225280593, 103.3233851476217], popup=kuantan_popup,
        icon=folium.Icon(color="black")
    ).add_to(m)
    folium.Marker(
        [3.315143565060173, 101.60099765655472], popup=kl_popup,
        icon=folium.Icon(color="cadetblue")
    ).add_to(m)
    folium.Marker(
        [5.320985318929512, 100.36447204836247], popup=penang_popup,
        icon=folium.Icon(color="orange")
    ).add_to(m)
    folium.Marker(
        [1.7958555965019127, 103.5584237529655], popup=johor_popup,
        icon=folium.Icon(color="darkgreen")
    ).add_to(m)

    st_folium(m, width=1025, returned_objects=[])
    

render_page()