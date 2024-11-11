import os
import openai
import streamlit as st
import time
from openai import OpenAI
import pandas as pd
from Survey_page import result

#get OpenAI key
openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()
st.markdown("""
    <style>
      section[data-testid="stSidebar"] {
        top: -7%; 
        height: 200% !important;
        background-color: #E3FFD5;
      }
    </style>""", unsafe_allow_html=True)
st.sidebar.image("pages/logo.png", use_column_width=True, caption=None)
#Trail Difficulty
st.markdown("# Trail Selection")

##delete me later :D (this is so we can easily navigate the pages while we work on it)
##if you want to display the pages then copy this one
st.sidebar.page_link("Survey_page.py", label= "Survey Page")
st.sidebar.page_link("pages/Personalized_plan.py", label="Personalized Plan")
st.sidebar.page_link("pages/transition.py", label="Transition Page")

# Load the dataset into a pandas DataFrame
data = pd.read_excel('pages/trail_list.xlsx')

#Trail Selection
with st.spinner("That's great to know! Here are some hikes you can go on"):
    if result['hiking_experience'] == 'Beginner':
        easy_trails = data[data['intensity_rating'] == 'Easy']
        # Select 3 random trails
        random_easy_trails = easy_trails.sample(n=3, replace=True) if len(easy_trails) >= 3 else easy_trails
        st.write(random_easy_trails)
    elif result['hiking_experience'] == 'Intermediate':
        int_trails = data[data['intensity_rating'] == 'Moderate']
        # Select 3 random trails
        random_int_trails = int_trails.sample(n=3, replace=True) if len(int_trails) >= 3 else int_trails
        st.write(random_int_trails)
    else:
        st.write("Whoops")
st.success("Here we go! Let's go outside")

#Location Map
st.markdown("# Location Map")
with st.form(key = "chat"):
    trail_selection = st.text_input(
        "Which trails do you want to go to?", 
        value=None, 
        placeholder="Enter trail name"
    )
    submitted = st.form_submit_button("Submit")
        
    if submitted:
        if trail_selection in data['trail_name'].values:
            selected_trail = data[data['trail_name'] == trail_selection]
            
            # Extract the first values from latitude and longitude columns
            lat = selected_trail['latitude'].iloc[0]
            lon = selected_trail['longitude'].iloc[0]

            # Update the DataFrame with the specific coordinates
            df = pd.DataFrame({
                'lat': [lat],
                'lon': [lon]
            })

            # Plot the map with the updated DataFrame
            st.map(df)
        else:
            st.error("Selected trail not found.")

#Plants and Terrain Prototype
def get_completion2(prompt, model="gpt-3.5-turbo"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role": "system", "content": "respond as a expert trail guide who offers \
         3 columns of information about the possible hike trail. One column will be\
         for the plants you may encounter on the hike, the middle column is for warning of\
         possible dangerous animals on that trail, and the third column is for the kind of terrain the trail is."},
        {"role": "user", "content": prompt},
        ]
    )
    return completion.choices[0].message.content

def get_image(prompt, model="dall-e-2"):
    n = 3   # Number of images to generate
    images = client.images.generate(
        prompt=f"Generate 3 images of the {prompt} based on the 3 columns\
              {get_completion2(prompt)}, first column should be about possible plants\
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

st.markdown("# Caution!")

# def get_completion(prompt, model="gpt-3.5-turbo"):
#     completion = client.chat.completions.create(
#         model=model,
#         messages=[
#         {"role": "system", "content": "respond as a expert trail guide who offers a detailed packing list of what to bring on the\
#          specific hike the user enters. Divide the response into three categoires: Absolutley necessary, Recommened, and If extra\
#          space.Place the information into a well-designed organized table."},
#         {"role": "user", "content": prompt},
#         ]
#     )
#     return completion.choices[0].message.content

# with st.form(key = "chat"):
#     prompt = st.text_input("", placeholder="e.g., Mission Peak") # TODO!
#     submitted = st.form_submit_button("What should I bring on the hike")
    
#     if submitted:
#         st.write(get_completion(prompt))