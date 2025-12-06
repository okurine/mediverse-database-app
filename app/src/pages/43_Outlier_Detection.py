import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()
st.title("📉 Outlier Detection")

API_URL = "http://web-api:4000/analyst/labresults/outliers"

try:
    resp = requests.get(API_URL)
    if resp.status_code == 200:
        st.table(resp.json())
    else:
        st.error(resp.text)
except Exception as e:
    st.error(e)
