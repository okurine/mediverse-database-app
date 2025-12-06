import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()
st.title("👥 User Provisioning")

API = "http://web-api:4000/admin"

def fetch_staff():
    r = requests.get(f"{API}/staff")
    return r.json() if r.status_code == 200 else []

staff = fetch_staff()

st.subheader("Existing Users")
st.table(staff)

st.markdown("---")
st.subheader("Create New Staff Member")

with st.form("staff_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    status = st.text_input("Status (active/inactive)")
    submit = st.form_submit_button("Create")

    if submit:
        payload = {"name": name, "email": email, "status": status}
        r = requests.post(f"{API}/staff", json=payload)
        if r.status_code == 201:
            st.success("Staff created.")
            st.experimental_rerun()
        else:
            st.error(r.text)
