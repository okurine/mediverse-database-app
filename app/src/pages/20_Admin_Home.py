import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title("🖥️ System Admin Home")
st.write("Welcome, administrator.")


if st.button('🔐 Role-Based Access Control', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_RBAC.py')

if st.button('📜 Audit Logs', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_Audit_Logs.py')
  
if st.button('📊 System Health Monitoring', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/23_System_Health.py')
  
if st.button('🔌 Integration Management', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/24_Integrations.py')
  
if st.button('🛡️ Security Alerts', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/25_Security_Alerts.py')
  
if st.button('👥 User Provisioning', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/26_User_Provisioning.py')
