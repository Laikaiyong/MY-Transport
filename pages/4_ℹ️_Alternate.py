import pandas as pd
from requests import get

import requests
import os
import json
import time
import random

import streamlit as st

def load_view():
    st.title("Alternative Choices")
    
    expander = st.expander("E-hailing")
    
    expander.title("Normal e-hailing")
    expander.write("Get a ride anywhere through product of digitalization")
    expander.image("https://images.squarespace-cdn.com/content/v1/5a5dbe4632601eb31977f947/1681799372539-PLPFXL099T1WX2VN6OJ8/MY-Step-4.jpg")
    
    expander.title("Carpool")
    expander.write("Decarbonization can be done through carpooling in e-hailing")
    expander.image("https://bm.technave.com/wp-content/uploads/2023/06/JustSave-Step-1-473x1024.png")

    
    expander = st.expander("Beam")
    expander.write("Get a ride by using pay-as-you-go bike")
    expander.image("https://assets-global.website-files.com/635f3b16f95dcc5f973a0585/6375f529cbef95dc03e4f448_637465528df3bb44154499c3_DSC05139.jpeg")
    
    expander = st.expander("Moovit")
    expander.write("Plan your journey with Moovit")
    expander.image("https://moovit.com/wp-content/uploads/2020/05/Screenshots-directions.png")

load_view()