import os
import pandas as pd
import streamlit as st 
from openai import OpenAI

#my-api-key-here
OpenAI.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI() 

data = pd.read_excel(r"C:\\Users\\brian\\OneDrive\\Documents\\trail_list.xlsx")

# create a wrapper function
def get_completion(prompt, model="gpt-3.5-turbo"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role": "system", "content": f"You're a hiking expert. Based on the length, elevation, and intensity of the hiking trails in {data},\
                                        sort the hiking equipment people would need to bring into a table. Use columns for trail difficulty and rows for equipment categories.\
                                        The difficulty levels are Easy, Moderate, and Challenging" },
        {"role": "user", "content": prompt},
        ]
    )
    return completion.choices[0].message.content

with st.form(key = "chat"):
    # add questions here
    prompt = st.text_area ("Hiking Material Request")
    submitted = st.form_submit_button("Submit")


    if submitted:
        st.write(get_completion(prompt))
