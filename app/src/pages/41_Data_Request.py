import streamlit as st
import requests
from modules.nav import SideBarLinks
from datetime import datetime

SideBarLinks()
st.title("🗂️ Data Access Requests")

API_URL = "http://web-api:4000/analyst/datarequests"

# ---------------- LIST REQUESTS ----------------
st.subheader("Existing Data Requests")

try:
    resp = requests.get(API_URL)
    if resp.status_code == 200:
        requests_list = resp.json()
        st.table(requests_list)
    else:
        st.error(f"API Error: {resp.text}")
except Exception as e:
    st.error(f"Error connecting to the API: {e}")

st.markdown("---")

# ---------------- CREATE REQUEST ----------------
st.subheader("Create New Request")

title = st.text_input("Title")
description = st.text_area("Description")
staff_id = st.number_input("Staff ID", min_value=1)
dateCreated = datetime.now().strftime("%Y-%m-%d")

if st.button("Submit Request", type="primary"):
    payload = {
        "title": title,
        "description": description,
        "staffId": staff_id,
        "dateCreated": dateCreated
    }
    try:
        r = requests.post(API_URL, json=payload)
        if r.status_code == 201:
            st.success("Request created successfully!")
            st.experimental_rerun()
        else:
            st.error(f"API Error: {r.text}")
    except Exception as e:
        st.error(f"Error submitting request: {e}")
