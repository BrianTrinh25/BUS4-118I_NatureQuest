import streamlit as st 
import requests
from openai import OpenAI

client = OpenAI(api_key="API Key") 
st.title("Packing List")
st.write("What Should You Bring")

def get_completion(prompt, model="gpt-3.5-turbo"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role": "system", "content": "respond as a expert trail guide who offers a detailed packing list of what to bring on the\
         specific hike the user enters. Divide the response into three categoires: Absolutley necessary, Recommened, and If extra\
         space.Place the information into a well-designed organized table."},
        {"role": "user", "content": prompt},
        ]
    )
    return completion.choices[0].message.content

with st.form(key = "chat"):
    prompt = st.text_input("", placeholder="e.g., Mission Peak") # TODO!
    submitted = st.form_submit_button("What should I bring on the hike")
    
    if submitted:
        st.write(get_completion(prompt))