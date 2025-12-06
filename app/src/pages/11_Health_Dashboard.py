import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

st.title("📊 My Health Dashboard")

SideBarLinks()

# Get patient_id from session state (set earlier from login)
patient_id = st.session_state.get("patient_id")

if patient_id is None:
    st.error("No patient_id selected.")
    st.button(
        "Return Home",
        on_click=lambda: st.switch_page("Home.py"),
    )
    st.stop()

# API endpoint
API_URL = f"http://web-api:4000/patient/patients/{patient_id}/dashboard"

try:
    response = requests.get(API_URL)

    if response.status_code != 200:
        st.error(f"API Error: {response.text}")
        st.stop()

    data = response.json()

    # -------------------------------
    # Patient Information Header
    # -------------------------------
    patient = data.get("patient", {})

    with st.container():
        st.subheader("👤 Patient Information")
        st.write(f"**Name:** {patient.get('name')}")
        st.write(f"**Gender:** {patient.get('gender')}")
        st.write(f"**DOB:** {patient.get('DOB')}")
        st.write(f"**Status:** {patient.get('status')}")

    st.markdown("---")

    # -------------------------------
    # Vitals
    # -------------------------------
    vitals = data.get("vitals", [])

    st.subheader("🩺 Vitals")

    if vitals:
        st.table([
            {
                "Type": v["type"],
                "Value": v["value"],
                "Timestamp": v["timestamp"]
            }
            for v in vitals
        ])
    else:
        st.info("No vitals found.")

    st.markdown("---")

    # -------------------------------
    # Care Plans
    # -------------------------------
    careplans = data.get("careplans", [])

    st.subheader("📘 Care Plans")

    if careplans:
        st.table([
            {
                "Goal": cp["goals"],
                "Start": cp["startTime"],
                "End": cp["endTime"],
                "Staff ID": cp["staffId"]
            }
            for cp in careplans
        ])
    else:
        st.info("No care plans found.")

    st.markdown("---")

    # -------------------------------
    # Lab Results
    # -------------------------------
    labs = data.get("labs", [])

    st.subheader("🧪 Lab Results")

    if labs:
        st.table([
            {
                "Lab Type": lab["labType"],
                "Value": lab["value"],
                "Date": lab["date"],
                "Outlier?": "Yes" if lab["isOutlier"] else "No",
                "Modified?": "Yes" if lab["isModified"] else "No"
            }
            for lab in labs
        ])
    else:
        st.info("No lab results found.")

    st.markdown("---")

    # -------------------------------
    # Treatments
    # -------------------------------
    treatments = data.get("treatments", [])

    st.subheader("💊 Treatments")

    if treatments:
        st.table([
            {
                "Type": t["type"],
                "Name": t["name"],
                "Dosage": t["dosage"],
                "Frequency": t["frequency"],
                "Start Date": t["startdate"],
                "End Date": t["endDate"],
            }
            for t in treatments
        ])
    else:
        st.info("No treatments found.")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running at http://web-api:4000")
