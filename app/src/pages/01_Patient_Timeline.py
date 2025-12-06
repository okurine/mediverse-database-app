import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()
st.title("📅 Unified Patient View")

patient_id = st.number_input("Enter Patient ID", min_value=1, step=1)

if patient_id is None:
    st.error("No patient_id selected.")
    st.stop()

API_URL = f"http://web-api:4000/clinician/patients/{patient_id}/timeline"

try:
    response = requests.get(API_URL)

    if response.status_code != 200:
        st.error(f"API Error: {response.text}")
        st.stop()

    data = response.json()

    st.header("Patient Info")
    st.table(data["patient"])

    st.markdown("---")
    st.header("Vitals")
    st.table(data["vitals"])

    st.markdown("---")
    st.header("Conditions")
    st.table(data["conditions"])

    st.markdown("---")
    st.header("Treatments")
    st.table(data["treatments"])

    st.markdown("---")
    st.header("Care Plans")
    st.table(data["careplans"])

    st.markdown("---")
    st.header("Appointments")
    st.table(data["appointments"])

    st.markdown("---")
    st.header("Lab Results")
    st.table(data["lab_results"])

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")


##############################
