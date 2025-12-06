import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()
st.title("💾 Project Data Export")

project_id = st.number_input("Enter Project ID", min_value=1)

API_URL = f"http://web-api:4000/analyst/projects/{project_id}/export"

if st.button("Export CSV"):
    try:
        resp = requests.get(API_URL)
        if resp.status_code == 200:
            csv_text = resp.json().get("csv", "")
            st.download_button("Download CSV", csv_text, "export.csv")
        else:
            st.error(resp.text)
    except Exception as e:
        st.error(e)
