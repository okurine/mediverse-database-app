import streamlit as st
import requests
from modules.nav import SideBarLinks
from datetime import datetime

SideBarLinks()
st.title("🔎 View Data")

id = st.number_input("Enter Project ID", min_value=1)

if st.button("View"):
    try:
        resp1 = requests.get(f"http://web-api:4000/analyst/projects/{id}/labs")
        st.subheader("Labs")
        if resp1.status_code == 200:
            st.table(resp1.json())
        else:
            st.error(resp1.text)
    except Exception as e:
        st.error(e)
    try:
        resp2 = requests.get(f"http://web-api:4000/analyst/projects/{id}/vitals")
        st.subheader("Vitals")
        if resp2.status_code == 200:
            st.table(resp2.json())
        else:
            st.error(resp2.text)
    except Exception as e:
        st.error(e)
        