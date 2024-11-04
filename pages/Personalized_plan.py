import os
import openai
import streamlit as st
import time
from openai import OpenAI
import pandas as pd
from Survey_page import hiking_experience, transportation, specific_features, solo_or_group, pet_on_trail, disability_check, time_check_start, time_check_end

#get OpenAI key
openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()

#Trail Difficulty
st.markdown("# Trail Difficulty Prototype")

##delete me later :D (this is so we can easily navigate the pages while we work on it)
##if you want to display the pages then copy this one
st.sidebar.page_link("Survey_page.py", label= "Survey Page")
st.sidebar.page_link("pages/Personalized_plan.py", label="Personalized Plan")
st.sidebar.page_link("pages/transition.py", label="Transition Page")

# Load the dataset into a pandas DataFrame
data = pd.read_csv('pages/trails_list.xlsx')

def get_completion(model="gpt-3.5-turbo"):
   completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role":"system",
         "content": f"Get information from {data}, based on {hiking_experience}, use the intensity column, suggest 3 random trails.\
            Suggest Easy for beginner, Moderate for Intermediate, Challenging for Advanced. Display a table where some additional information\
            are considered:  shuttle_possible for people with {transportation} transportation if no, dog_allowed or not if yes on {pet_on_trail}\
"},
        ]
    )
   return completion.choices[0].message.content

with st.spinner("That's great to know! Here are some hikes you can go on"):
    st.write(get_completion())
st.success("Here we go! Let's go outside")

#Hiking Map
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

#Plants and Terrain Prototype
def get_completion(prompt, model="gpt-3.5-turbo"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role": "system", "content": "respond as a expert trail guide who offers \
         3 columns of information about the possible hike trail. One column will be\
         for the plants you may encounter on the hike, the middle column is for warning of\
         possible dangerous animals on that trail, and the third column is for terrain, for example a lot of incline\
         which is usually over 1200 ft elevation gain, or easy under 800ft gain or a lot\
         of woodland or barren land."},
        {"role": "user", "content": prompt},
        ]
    )
    return completion.choices[0].message.content

def get_image(prompt, model="dall-e-2"):
    n = 3   # Number of images to generate
    images = client.images.generate(
        prompt=f"Generate 3 images of the {prompt} based on the 3 columns\
              {get_completion(prompt)}, first column should be about possible plants\
                one might see on the trail, second is possible animal, third is the terrain",
        model=model,
        n=n,
        size="1024x1024"
    )
    return [image.url for image in images.data]

with st.form(key = "chat"):
    prompt = st.text_input("Which trail would you like to go to?")
    submitted = st.form_submit_button("Submit")
        
    if submitted:
        st.write(get_completion(prompt))
        
        urls = get_image(prompt)

        st.subheader('Here are additional informations:', divider='grey')
        col1, col2, col3 = st.columns(3)

        with col1:
            st.header("Plants")
            st.image(urls[0], caption= f'Possible Plants and Flora', use_column_width=True) 

        with col2:
            st.header("Animals")
            st.image(urls[1], caption= f'Animals Encounter', use_column_width=True) 

        with col3:
            st.header("Terrain")
            st.image(urls[2], caption= f'Hiking Terrain', use_column_width=True) 
