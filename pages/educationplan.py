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

prompt = st.session_state.selectedTrailName

st.sidebar.image("pages/logo.png", use_column_width=True, caption=None)
st.sidebar.page_link("pages/Personalized_plan.py", label="Personalized Plan")
st.sidebar.page_link("pages/packinginfo.py", label = "Packing Info")
st.sidebar.page_link("pages/educationplan.py", label = "Education Plan")
st.title("Education Page")
st.write(f"How can you treat the environment properly on this hike at {prompt}?")
st.sidebar.markdown("# Education Page")

def get_completion(prompt, model="gpt-3.5-turbo"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role": "system", "content": f"Respond as a local expert on environments, including floral and plants and water in creekside,\
         based on this specific hike {prompt}, give educational advice on how to keep the environement clean for the water,\
         how to protect the local floral and plants on that hike, and how to respect the environment in general. Present the advice in\
         numbered list with heading for each section"},
        {"role": "user", "content": prompt},
        ]
    )
    return completion.choices[0].message.content

st.write(get_completion(prompt))