import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()
st.title("🧠 Smart Notes Integration")

action = st.text_area("Action Taken")
outcome = st.text_area("Outcome Summary")
staff_id = st.number_input("Staff ID", min_value=1)

if st.button("Save Note"):
    payload = {
        "action": action,
        "outcome": outcome,
        "staffId": staff_id
    }

    response = requests.post("http://web-api:4000/clinician/notes", json=payload)

    if response.status_code == 201:
        st.success("Smart Note Saved!")
    else:
        st.error(response.text)
