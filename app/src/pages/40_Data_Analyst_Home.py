import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Data Analyst, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('🗂️ Data Access Requests', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/41_Data_Request.py')

if st.button('📚 Organize Projects', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/42_Data_Organization.py')
  
if st.button('📉 Outlier Detection', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/43_Outlier_Detection.py')
  
if st.button('❓ Missing Data', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/44_Missing_Data.py')
  
if st.button('💾 Data Export & Storage', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/45_Data_Exports.py')

if st.button('📊 Data Visualization Tools', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/46_Visualizations.py')

if st.button('🔎 View Data', 
            type='primary',
            use_container_width=True):
  st.switch_page('pages/47_view_data.py')

