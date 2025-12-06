import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()
st.title("📊 System Health Monitoring")

API_URL = "http://web-api:4000/admin/system/health"

try:
    r = requests.get(API_URL)
    if r.status_code != 200:
        st.error(r.text)
    else:
        data = r.json()
        st.json(data)

except Exception as e:
    st.error(f"API connection error: {e}")
