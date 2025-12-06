import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown(
    """
   MediVerse is a data driven healthcare intelligence platform designed to unify fragmented clinical, operational, and patient generated data into actionable insights. We’re building a secure, AI powered system that empowers hospitals, researchers, clinicians, patients, and system administrators to collaborate, analyze, and act without drowning in complexity. By streamlining data access, cleaning, and visualization, MediVerse helps users make smarter decisions in real time.

   Existing healthcare systems are siloed, slow, and often require manual workarounds to extract even basic insights. MediVerse solves this by offering intuitive data request workflows, built-in outlier and gap detection, and no code analytics dashboards. Whether you're a researcher organizing cohorts, a clinician tracking patient trends, or an admin managing secure access, MediVerse delivers clarity, control, and speed, making it the go to intelligence layer for modern care delivery.

    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
