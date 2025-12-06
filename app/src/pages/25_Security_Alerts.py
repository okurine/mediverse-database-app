import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

st.title("🛡️ Security Alerts")

API_URL = "http://web-api:4000/admin/alerts/system"

try:
    r = requests.get(API_URL)
    if r.status_code != 200:
        st.error(r.text)
    else:
        st.table(r.json())

except Exception as e:
    st.error(f"Connection failed: {e}")
