import os
import openai
import streamlit as st
from openai import OpenAI

openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()

def get_completion(prompt, model="gpt-3.5-turbo"):
   completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role":"system",
         "content": "You are a hiking expert.  Choose a specific hiking trail based on the hiker's choice of difficulty."},
        {"role": "user",
         "content": difficulty},
        ]
    )
   return completion.choices[0].message.content

# create our streamlit app


with st.form(key = "chat"):
    difficulty = st.radio('Select Difficulty', ['Easy', 'Medium', 'Hard'])
    #prompt = st.text_input("Enter your ideal difficulty level: ") 
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write(get_completion(difficulty))

