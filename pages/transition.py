import streamlit as st
st.markdown("""
    <style>
      section[data-testid="stSidebar"] {
        top: -7%; 
        height: 200% !important;
        background-color: #E3FFD5;
      }
    </style>""", unsafe_allow_html=True)
st.sidebar.image("pages/logo.png", use_column_width=True, caption=None)

st.markdown('# Are you ready to go hiking?')
st.page_link("Survey_page.py", label="Adjust Survey", icon="✏️")
st.page_link("pages/Personalized_plan.py", label="Your Personalized Plan", icon="💡")
