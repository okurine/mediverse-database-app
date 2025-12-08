# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


## ------------------------ Examples for Role of patient ------------------------

def patientHomeNav():
    st.sidebar.page_link(
      "pages/10_patient_Home.py", label="Patient Home", icon="👤"
    )
    
#### ------------------------ Examples for Role of clinician ------------------------
def clinicianHomeNav():
    st.sidebar.page_link(
        "pages/00_Clinician_Home.py", label="Clinition Home", icon="🏠"
    )


## ------------------------ Examples for Role of Data Analyst ------------------------

def dataAnalystHomeNav():
    st.sidebar.page_link(
      "pages/40_Data_Analyst_Home.py", label="Data Analyst Home", icon="👤"
    )




#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin", icon="🖥️")
    st.sidebar.page_link(
        "pages/21_ML_Model_Mgmt.py", label="ML Model Management", icon="🏢"
    )


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=550)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show clinician if the user is a clinician role.
        if st.session_state["role"] == "clinician":
            HomeNav()    
            clinicianHomeNav()
           
        # Show Data analyst if the user is a analyst role.
        if st.session_state["role"] == "analyst":
            HomeNav()
            dataAnalystHomeNav()
           
        # If the user role is patient, show the patient page
        if st.session_state["role"] == "patient":
            HomeNav()
            patientHomeNav()
  
        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "administrator":
            HomeNav()
            AdminPageNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
