import streamlit as st
import requests
from modules.nav import SideBarLinks
from datetime import datetime

SideBarLinks()
st.title("📚 Project Management")

API_URL = "http://web-api:4000/analyst/projects"

# ---------------- LIST PROJECTS ----------------
st.subheader("Projects")

try:
    resp = requests.get(API_URL)
    if resp.status_code == 200:
        st.table(resp.json())
    else:
        st.error(resp.text)
except Exception as e:
    st.error(e)

st.markdown("---")

# ---------------- CREATE PROJECT ----------------
st.subheader("Create New Project")

name = st.text_input("Project Name")
start = st.date_input("Start Date")
end = st.date_input("End Date")
requestId = st.number_input("Related Request ID", min_value=1)

if st.button("Create Project", type="primary"):
    payload = {
        "name": name,
        "startDate": str(start),
        "endDate": str(end),
        "requestId": requestId
    }
    try:
        r = requests.post(API_URL, json=payload)
        if r.status_code == 201:
            st.success("Project created")
            st.experimental_rerun()
        else:
            st.error(r.text)
    except Exception as e:
        st.error(e)
