import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()
st.title("❓ Missing Data Reports")

check_type = st.selectbox(
    "Check Missing:",
    ["demographics", "vitals", "labs"]
)

API_URL = f"http://web-api:4000/analyst/patients/missing?check={check_type}"

try:
    resp = requests.get(API_URL)
    if resp.status_code == 200:
        st.table(resp.json())
    else:
        st.error(resp.text)
except Exception as e:
    st.error(e)
