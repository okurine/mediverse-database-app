import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()
st.title("📝 Care Plan Management")

st.subheader("Lookup Patient Care Plans")
patient_id = st.number_input("Enter Patient ID", min_value=1)

if st.button("Fetch Care Plans"):
    API_URL = f"http://web-api:4000/clinician/patients/{patient_id}/timeline"
    response = requests.get(API_URL)

    if response.status_code == 200:
        data = response.json()
        st.table(data["careplans"])
    else:
        st.error("Unable to load care plans")

st.markdown("---")
st.subheader("Create New Care Plan")

goals = st.text_input("Care Plan Goals")
start = st.text_input("Start Time (YYYY-MM-DD)")
end = st.text_input("End Time (YYYY-MM-DD, optional)")
staff_id = st.number_input("Staff ID", min_value=1, step=1)

if st.button("Create Care Plan"):
    payload = {
        "goals": goals,
        "startTime": start,
        "endTime": end or None,
        "staffId": staff_id,
        "patientId": patient_id
    }

    response = requests.post("http://web-api:4000/clinician/careplans", json=payload)

    if response.status_code == 201:
        st.success("Care Plan Created")
    else:
        st.error(response.text)


st.markdown("---")
st.subheader("Update Existing Care Plan")

update_id = st.number_input("Care Plan ID to Update", min_value=1, step=1)
new_goals = st.text_input("Updated Goals (optional)")
new_start = st.text_input("Updated Start Time (optional)")
new_end = st.text_input("Updated End Time (optional)")
new_staff = st.text_input("Updated Staff ID (optional)")

if st.button("Update Care Plan"):
    payload = {}

    if new_goals:
        payload["goals"] = new_goals
    if new_start:
        payload["startTime"] = new_start
    if new_end:
        payload["endTime"] = new_end
    if new_staff:
        payload["staffId"] = new_staff

    response = requests.put(f"http://web-api:4000/clinician/careplans/{update_id}", json=payload)

    if response.status_code == 200:
        st.success("Care Plan Updated")
    else:
        st.error(response.text)
