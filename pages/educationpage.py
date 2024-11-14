import streamlit as st 
import requests
import os
import openai
from openai import OpenAI
client = OpenAI()
openai.api_key = os.environ["OPENAI_API_KEY"] 
st.markdown("""
    <style>
      section[data-testid="stSidebar"] {
        top: -7%; 
        height: 200% !important;
        background-color: #E3FFD5;
      }
    </style>""", unsafe_allow_html=True)
if "rerun3" not in st.session_state:
    st.session_state.rerun3 = True
if st.session_state.rerun3 is True:
    st.session_state.rerun3 = False
    st.rerun()

st.sidebar.image("pages/logo.png", use_column_width=True, caption=None)
st.sidebar.page_link("pages/Personalized_plan.py", label="Personalized Plan")
st.sidebar.page_link("pages/packinginfo.py", label = "Packing Info")
st.sidebar.page_link("pages/educationplan.py", label = "Education Plan")
st.title("Education Page")
st.write("How can you treat the environment properly?")
st.sidebar.markdown("# Education Page")