import streamlit as st
from clinician_routes import get_patient, get_vitals, get_careplans


st.title("📅 Unified Patient View")

patient_id = st.number_input("Enter Patient ID", min_value=1, step=1)

if patient_id:
    patient = get_patient(patient_id)
    if not patient:
        st.error("Patient not found")
    else:
        st.subheader(f"Patient: {patient['name']} ({patient['gender']})")
        st.write(f"DOB: {patient['DOB']}")
        st.write(f"Status: {patient['status']}")

        st.subheader("Vitals")
        vitals = get_vitals(patient_id)
        st.table(vitals)

        st.subheader("Care Plans")
        careplans = get_careplans(patient_id)
        st.table(careplans)
