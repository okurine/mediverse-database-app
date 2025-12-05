import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Patient, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('📋 Health Overview', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Health_Dashboard.py')

if st.button('📘 My Care Plans', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_Patient_Care_Plans.py')

if st.button('💉 Treatment Overview', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_Treatment_Overview.py')

