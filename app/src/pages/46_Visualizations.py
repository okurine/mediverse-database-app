import streamlit as st
import requests
from modules.nav import SideBarLinks
from datetime import datetime

SideBarLinks()
st.title("📊 Visualization Tools")

# ------------ LIST VISUALIZATIONS ------------
st.subheader("Existing Visualizations")

API_LIST = "http://web-api:4000/analyst/visualizations"
try:
    resp = requests.get(API_LIST)
    if resp.status_code == 200:
        st.table(resp.json())
    else:
        st.error(resp.text)
except Exception as e:
    st.error(e)

st.markdown("---")

# ------------ CREATE VISUALIZATION ------------
st.subheader("Create Visualization")

v_type = st.selectbox("Type", ["line", "bar", "heatmap", "scatter"])
summary = st.text_area("Summary")
projectId = st.number_input("Project ID", min_value=1)
dateCreated = datetime.now().strftime("%Y-%m-%d")

if st.button("Create Visualization", type="primary"):
    payload = {
        "type": v_type,
        "summary": summary,
        "projectId": projectId,
        "dateCreated": dateCreated,
    }
    try:
        r = requests.post(API_LIST, json=payload)
        if r.status_code == 201:
            st.success("Visualization created!")
            st.experimental_rerun()
        else:
            st.error(r.text)
    except Exception as e:
        st.error(e)
