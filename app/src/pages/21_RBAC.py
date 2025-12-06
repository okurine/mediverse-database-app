import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()
st.title("🔐 Role-Based Access Control")

API_BASE = "http://web-api:4000/admin"

# --- Fetch roles ---
def fetch_roles():
    r = requests.get(f"{API_BASE}/roles")
    return r.json() if r.status_code == 200 else []

# --- Fetch permissions ---
def fetch_permissions():
    r = requests.get(f"{API_BASE}/permissions")
    return r.json() if r.status_code == 200 else []

roles = fetch_roles()
permissions = fetch_permissions()

st.subheader("Existing Roles")
st.table(roles)

st.markdown("---")
st.subheader("Create New Role")

with st.form("create_role_form"):
    role_id = st.number_input("Role ID", min_value=1, step=1)
    role_name = st.text_input("Role Name")
    desc = st.text_input("Description")
    perm_id = st.number_input("Permission ID", min_value=1, step=1)
    submitted = st.form_submit_button("Create Role")

    if submitted:
        payload = {
            "roleId": int(role_id),
            "name": role_name,
            "description": desc,
            "permissionId": int(perm_id),
        }
        r = requests.post(f"{API_BASE}/roles", json=payload)
        if r.status_code == 201:
            st.success("Role created.")
            st.experimental_rerun()
        else:
            st.error(r.text)

st.markdown("---")
st.subheader("Create Permission")

with st.form("create_perm_form"):
    permission_id = st.number_input("Permission ID", min_value=1, step=1)
    action = st.text_input("Action")
    resource = st.text_input("Resource")
    submit_perm = st.form_submit_button("Create Permission")

    if submit_perm:
        payload = {
            "permissionId": int(permission_id),
            "action": action,
            "resource": resource,
        }
        r = requests.post(f"{API_BASE}/permissions", json=payload)
        if r.status_code == 201:
            st.success("Permission created.")
            st.experimental_rerun()
        else:
            st.error(r.text)
