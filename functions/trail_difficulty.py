import os
import openai
import streamlit as st
import time
from openai import OpenAI

openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()

def get_completion(prompt, model="gpt-3.5-turbo"):
   completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role":"system",
         "content": f"Recommend specific easy, medium, and hard trails the hiker can explore within California.\
        Organize the information into a three-column table. Include details on location, trail name, terrain, elevation, trail length, and landmarks.\
        Make sure to recommend trails relevant to the hiker's {difficulty}."},
        {"role": "user",
         "content": difficulty},
        ]
    )
   return completion.choices[0].message.content

# create our streamlit app

with st.form(key = "chat"):
    difficulty = st.radio('What is your hiking trail experience?', ['Beginner', 'Intermediate', 'Expert'])    
    submitted = st.form_submit_button("Submit")
        
    if submitted:
        with st.spinner("That's great to hear! Here are some hikes you can go on"):
            time.sleep(5)
        st.success("Generating your recommendations...")
        st.write(get_completion(difficulty))

