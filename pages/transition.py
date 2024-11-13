import streamlit as st
from Survey_page import result

st.markdown("""
    <style>
      section[data-testid="stSidebar"] {
        top: -7%; 
        height: 200% !important;
        background-color: #E3FFD5;
      }
    </style>""", unsafe_allow_html=True)
st.sidebar.image("pages/logo.png", use_column_width=True, caption=None)

#check if survey has been fully completed
if result['hiking_before'] == "" or result['specific_features'] == "" or result['pet_on_trail'] == "" or result['disability_check'] == "" or result['time_check_start'] == "" or result['time_check_end'] == "": 
  st.error("Error! You left one or more questions blank on the survey! Please review.")
  st.page_link("Survey_page.py", label="Adjust Survey", icon="✏️")
else: 
  st.markdown('# Are you ready to go hiking?')
  st.page_link("Survey_page.py", label="Adjust Survey", icon="✏️")
  st.page_link("pages/Personalized_plan.py", label="Your Personalized Plan", icon="💡")
