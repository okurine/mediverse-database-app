import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
from datetime import datetime

st.title("📘 My Care Plans")

SideBarLinks()

# Get patient_id from session state (set earlier during login)
patient_id = st.session_state.get("patient_id")

if patient_id is None:
    st.error("No patient_id selected.")
    st.button(
        "Return Home",
        on_click=lambda: st.switch_page("Home.py"),
    )
    st.stop()

# API endpoint
API_URL = f"http://web-api:4000/patient/patients/{patient_id}/careplans"

def format_date(dt):
    try:
        return datetime.strptime(dt, "%a, %d %b %Y %H:%M:%S GMT").strftime("%Y-%m-%d")
    except:
        return dt

try:
    response = requests.get(API_URL)

    if response.status_code != 200:
        st.error(f"API Error: {response.text}")
        st.stop()

    careplans = response.json()  # List of care plans

    st.subheader("Your Care Plans")

    if not careplans:
        st.info("No care plans found.")
        st.stop()

    # Display table
    table_data = [
        {
            "Care Plan ID": c["carePlanId"],
            "Goal": c["goals"],
            "Start": format_date(c["startTime"]),
            "End": format_date(c["endTime"]),
        }
        for c in careplans
    ]

    st.table(table_data)

    st.subheader("Details")
    for c in careplans:
        with st.expander(f"Care Plan #{c['carePlanId']} - {c['goals']}"):
            st.write(f"**Goal:** {c['goals']}")
            st.write(f"**Start Time:** {format_date(c['startTime'])}")
            st.write(f"**End Time:** {format_date(c['endTime'])}")
            st.write(f"**Assigned Staff ID:** {c['staffId']}")
            st.write(f"**Patient ID:** {c['patientId']}")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running at http://web-api:4000")
