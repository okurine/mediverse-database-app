import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
from datetime import datetime

st.title("💉 Treatment Overview")

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
API_URL = f"http://web-api:4000/patient/patients/{patient_id}/treatments"

def format_date(dt):
    """Convert 'Tue, 24 Nov 2026 08:00:00 GMT' into '2026-11-24'."""
    try:
        return datetime.strptime(dt, "%a, %d %b %Y %H:%M:%S GMT").strftime("%Y-%m-%d")
    except:
        return dt

try:
    response = requests.get(API_URL)

    if response.status_code != 200:
        st.error(f"API Error: {response.text}")
        st.stop()

    treatments = response.json()   # List of treatments
    st.subheader("Your Treatments")

    if not treatments:
        st.info("No treatments found.")
        st.stop()

    # Build table data
    table_data = [
        {
            "Treatment ID": t["treatmentId"],
            "Name": t["name"],
            "Type": t["type"],
            "Dosage": t["dosage"],
            "Frequency": t["frequency"],
            "Start": format_date(t["startdate"]),
            "End": format_date(t["endDate"]),
        }
        for t in treatments
    ]

    # Show table
    st.table(table_data)

    # Detailed Section
    st.subheader("Details")
    for t in treatments:
        with st.expander(f"{t['name']} ({t['type']})"):
            st.write(f"**Treatment ID:** {t['treatmentId']}")
            st.write(f"**Name:** {t['name']}")
            st.write(f"**Type:** {t['type']}")
            st.write(f"**Dosage:** {t['dosage']}")
            st.write(f"**Frequency:** {t['frequency']}")
            st.write(f"**Start Date:** {format_date(t['startdate'])}")
            st.write(f"**End Date:** {format_date(t['endDate'])}")
            st.write(f"**Patient ID:** {t['patientId']}")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running at http://web-api:4000")
