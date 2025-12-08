import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()
st.title("📉 Outlier Detection")

API_URL = "http://web-api:4000/analyst/labresults/outliers"


# -------- displaying outlier values -------
try:
    resp = requests.get(API_URL)
    if resp.status_code == 200:
        st.table(resp.json())
    else:
        st.error(resp.text)
except Exception as e:
    st.error(e)

# -------- ability to update an outlier value ---------
st.subheader("Update Value")

# taking in the user input of values 
lab_id = st.number_input("Enter Lab Result ID", min_value=1)
val = st.number_input("Enter Modified Value (optional)")
date = st.date_input("Enter New Date (optional)")

if st.button("update", type="primary"):
    # adding the values to the payload if they exist (plus making sure it sets the value as modified)
    payload = {"isModified": 1}
    if val:
        payload["value"] = val
    if date:
        payload["date"] = date 
    
    try: 
        resp2 = requests.put(f"http://web-api:4000/analyst/labresults/{lab_id}", json=payload) 

        if resp2.status_code == 200:
            st.success("Updated Successfully")
        else:
            st.error(resp2.text)
    except Exception as e:
        st.error(e)