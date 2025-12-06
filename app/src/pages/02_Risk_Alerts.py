import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()
st.title("⚠️ Risk Alerts")

API_URL = "http://web-api:4000/clinician/risk"

try:
    response = requests.get(API_URL)

    if response.status_code != 200:
        st.error(f"API Error: {response.text}")
        st.stop()

    alerts = response.json()

    if not alerts:
        st.info("No current alerts.")
        st.stop()

    st.table(alerts)

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
