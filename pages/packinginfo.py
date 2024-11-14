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
if "rerun2" not in st.session_state:
    st.session_state.rerun2 = True
if st.session_state.rerun2 is True:
    st.session_state.rerun2 = False
    st.rerun()

st.sidebar.image("pages/logo.png", use_column_width=True, caption=None)
st.sidebar.page_link("pages/Personalized_plan.py", label="Personalized Plan")
st.sidebar.page_link("pages/packinginfo.py", label = "Packing Info")
st.sidebar.write("insert educational page here")
st.title("Packing List")
st.write("What Should You Bring")
st.sidebar.markdown("# Here's some supplies you should bring on the hike!")
prompt = st.session_state.selectedTrailName
def get_completion(prompt, model="gpt-3.5-turbo"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role": "system", "content": f"Respond as a expert trail guide who offers a detailed packing list of what to bring on the\
         specific hike {prompt}. Divide the response into three categories: Absolutely Necessary, Recommend, and If extra\
         space. Place the information into a well-designed organized table, with exactly one item per box. Above the table instead of replying with anything like certainly or anything just\
         say Here is a detailed packing list of items you can bring for the hike: *instead of the message between the two asterisks add the hike from the prompt*"},
        {"role": "user", "content": prompt},
        ]
    )
    return completion.choices[0].message.content

st.write(get_completion(prompt))