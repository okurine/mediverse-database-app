import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()
st.title("📱 Mobile Access")

st.info("""
Your EHR platform supports secure mobile access for clinicians.

- View Patient Timeline  
- Review Alerts  
- Update Care Plans  
- Add Smart Notes  
- Manage Medications  

Download the mobile app from your internal system portal.
""")