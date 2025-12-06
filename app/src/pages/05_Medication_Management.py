import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()
st.title("💊 Medication Tracking")

st.subheader("View Patient Medications")
patient_id = st.number_input("Enter Patient ID", min_value=1)

if st.button("Fetch Medications"):
    API_URL = f"http://web-api:4000/clinician/medications/{patient_id}"
    response = requests.get(API_URL)

    if response.status_code == 200:
        st.table(response.json())
    else:
        st.error(response.text)

st.markdown("---")
st.subheader("Add New Medication")

treatment_id = st.number_input("Treatment ID", min_value=1)
med_type = st.text_input("Type")
name = st.text_input("Medication Name")
dosage = st.text_input("Dosage")
frequency = st.text_input("Frequency")
startdate = st.text_input("Start Date (YYYY-MM-DD)")
enddate = st.text_input("End Date (YYYY-MM-DD)")

if st.button("Add Medication"):
    payload = {
        "treatmentId": treatment_id,
        "type": med_type,
        "name": name,
        "dosage": dosage,
        "frequency": frequency,
        "startdate": startdate,
        "endDate": enddate,
        "patientId": patient_id
    }

    response = requests.post("http://web-api:4000/clinician/medications", json=payload)

    if response.status_code == 201:
        st.success("Medication Added!")
    else:
        st.error(response.text)
