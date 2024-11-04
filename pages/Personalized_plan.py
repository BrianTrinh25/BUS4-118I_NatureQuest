import os
import openai
import streamlit as st
import time
from openai import OpenAI
import pandas as pd
import Survey_page

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
data = pd.read_excel('pages/trails_list.xlsx')

def get_completion1(model="gpt-3.5-turbo"):
   completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role":"system",
         "content": f"Get information from {data}, suggest 3 random trails based on the user level {prompt1}, use the intensity column\
            Only suggest Easy for beginner, Moderate for Intermediate, Challenging for Advanced. Display a table where some additional information\
            are considered: trail_name, show the corresponding column for hike_length, shuttle_possible for people with no transportation, dog_allowed Yes or No"},
        ]
    )
   return completion.choices[0].message.content

with st.form(key = "chat1"):
    prompt1 = st.text_input("Level? Beginner, Intermediate, Advanced")
    submitted = st.form_submit_button("Submit")
        
    if submitted:
        with st.spinner("That's great to know! Here are some hikes you can go on"):
            st.write(get_completion1())
        st.success("Here we go! Let's go outside")

#Hiking Map
st.markdown("# Hiking Map Prototype")

trail_selection = st.text_input(
    "Which trails do you want to go to?", value=None, placeholder= None
)

# Update your DataFrame with the specific coordinates
df = pd.DataFrame({
    'lat': [37.1936853],
    'lon': [-121.8389462]
})

# Plot the map with the updated DataFrame
st.map(df)

#Plants and Terrain Prototype
def get_completion2(prompt, model="gpt-3.5-turbo"):
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
              {get_completion1(prompt)}, first column should be about possible plants\
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
        st.write(get_completion2(prompt))
        
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
