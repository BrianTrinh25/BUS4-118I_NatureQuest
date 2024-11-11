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
    elif result['hiking_experience'] == 'Advanced':
        diff_trails = data[data['intensity_rating'] == 'Challenging']
        # Select 3 random trails
        random_diff_trails = diff_trails.sample(n=3, replace=True) if len(diff_trails) >= 3 else diff_trails
        st.write(random_diff_trails)
    else:
        st.write("Whoops")
st.success("Here we go! Let's go outside")

trail_selection = ""

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
# Assume trail_selection is defined elsewhere in the code
# Example: trail_selection = "Golden Gate Bridge: Presidio to Marin Headlands"
def get_completion2(model="gpt-3.5-turbo"):
    prompt = f"Provide information about the trail {trail_selection}, with three columns: \
              plants you may encounter, possible dangerous animals on the trail, and the terrain type."
    
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Respond as an expert trail guide offering three columns of information."},
            {"role": "user", "content": prompt},
        ]
    )
    return completion.choices[0].message.content

def get_image(model="dall-e-2"):
    # Get the completion from get_completion2
    completion_text = get_completion2()
    
    # Form the image prompt based on the text response
    image_prompt = f"Generate 3 images of the trail {trail_selection} based on the following details:\n\
                     Plants one might see: {completion_text.splitlines()[0]},\n\
                     Possible animals: {completion_text.splitlines()[1]},\n\
                     Terrain: {completion_text.splitlines()[2]}."

    images = client.images.generate(
        prompt=image_prompt,
        model=model,
        n=3,
        size="1024x1024"
    )
    return [image.url for image in images.data]

# Display text completion
if trail_selection != None:
    trail_description = get_completion2()
    st.write(trail_description)

# Generate and display images
if trail_selection != None:
    urls = get_image()

    st.subheader('Here is some additional information:', divider='grey')
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

# st.markdown("# Caution!")

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