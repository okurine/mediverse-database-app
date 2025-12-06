import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()
API = "http://web-api:4000/admin"

st.title("🔌 Integrations")

# Fetch existing integrations
def fetch_integrations():
    r = requests.get(f"{API}/integrations")
    return r.json() if r.status_code == 200 else []

integrations = fetch_integrations()

st.subheader("Existing Integrations")
st.table(integrations)

st.markdown("---")
st.subheader("Create New Integration")

with st.form("integration_form"):
    name = st.text_input("System Name")
    status = st.text_input("Status")
    last_sync = st.date_input("Last Sync Date")
    dept_id = st.number_input("Department ID", min_value=1)
    submit = st.form_submit_button("Create Integration")

    if submit:
        payload = {
            "systemName": name,
            "status": status,
            "lastSyncDate": str(last_sync),
            "departmentId": int(dept_id),
        }
        r = requests.post(f"{API}/integrations", json=payload)
        if r.status_code == 201:
            st.success("Integration added.")
            st.experimental_rerun()
        else:
            st.error(r.text)
