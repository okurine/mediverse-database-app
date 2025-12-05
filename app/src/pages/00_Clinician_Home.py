import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Clinician, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('📅 Unified Patient View', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Patient_Timeline.py')

if st.button('⚠️ Risk Alerts', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Risk_Alerts.py')
  
if st.button('📝 Care Plan Management', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/03_Care_Plans.py')

if st.button('🧠 Smart Notes Integration', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/04_Smart_Notes.py')

if st.button('💊 Medication Tracking', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/05_Medication_Management.py')

if st.button('📱 Mobile Access', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/06_Mobile_Access.py')