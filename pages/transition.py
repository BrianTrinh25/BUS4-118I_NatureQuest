import streamlit as st

##delete me later :D (this is so we can easily navigate the pages while we work on it)
##if you want to display the pages then copy this one
st.sidebar.page_link("Survey_page.py", label= "Survey Page")
st.sidebar.page_link("pages/Personalized_plan.py", label="Personalized Plan")
st.sidebar.page_link("pages/transition.py", label="Transition Page")

st.markdown('# Are you ready to go hiking?')
st.page_link("Survey_page.py", label="Adjust Survey", icon="✏️")
st.page_link("pages/Personalized_plan.py", label="Your Personalized Plan", icon="💡")
