import os
import openai
import streamlit as st
import time
from openai import OpenAI
import pandas as pd
from Survey_page import hiking_before

#get OpenAI key
openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()

#Trail Difficulty
def get_completion(model="gpt-3.5-turbo"):
   completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role":"system",
         "content": f"Recommend specific easy, medium, and hard trails the hiker can explore within California.\
        Organize the information into a three-column table. Include details on location, trail name, terrain, elevation, trail length, and landmarks.\
        Make sure to recommend trails relevant to the hiker level, which is {hiking_before}."},
        ]
    )
   return completion.choices[0].message.content


st.write(get_completion())
with st.spinner("That's great to hear! Here are some hikes you can go on"):
    time.sleep(5)
st.success("Here we go! Let's go outside")

st.markdown("# Hiking Map Prototype")

zip = st.number_input(
    "Zip code", value=None, placeholder="Zip Code"
)

distance = st.selectbox(
    "Distance",
    ("5 mi", "10 mi", "25 mi", "50 mi"),
)

# Update your DataFrame with the specific coordinates
df = pd.DataFrame({
    'lat': [37.307226530422035, 37.269817968115234, 37.445452198845956, 37.42591903699686, 37.3954045204858, 37.293801584395865, 37.23301521261931],
    'lon': [-121.9137624590682, -121.94942483361638, -121.84741556130625, -121.92485823400975, -121.82525695742902, -122.04148682149903, -121.92715082443866]
})

# Plot the map with the updated DataFrame
st.map(df)