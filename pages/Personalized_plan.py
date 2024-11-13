import os
import openai
import streamlit as st
import time
from openai import OpenAI
import pandas as pd
from Survey_page import result

# Initialize session state if nonexisting
if 'selected_trail' not in st.session_state:
    st.session_state.selected_trail = None
if 'show_details' not in st.session_state:
    st.session_state.show_details = False
if 'trail_options' not in st.session_state:
    st.session_state.trail_options = None
if 'selected_trail_name' not in st.session_state:
    st.session_state.selected_trail_name = None

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

st.markdown("# Trail Selection")
# Load the dataset into a pandas DataFrame
data = pd.read_excel('pages/trail_list.xlsx')

learnMoreOption = ""
trail_selection = ""

# Define callback functions for buttons
def show_trail_details(trail_option):
    st.session_state.selected_trail = trail_option
    st.session_state.show_details = True

#Trail Selection
st.success("Here we go! Let's go outside!")
with st.spinner("That's great to know! Here are some hikes you can go on"):
    # Select 3 random trails
    if st.session_state.trail_options is None:
        # Select 3 random trails for Beginner
        if result['hiking_experience'] == 'Beginner':
            easy_trails = data[data['intensity_rating'] == 'Easy']
            random_easy_trails = easy_trails.sample(n=3, replace=True) if len(easy_trails) >= 3 else easy_trails
            st.session_state.trail_options = {
                'option1': random_easy_trails.iloc[0],
                'option2': random_easy_trails.iloc[1],
                'option3': random_easy_trails.iloc[2],
                'name1': random_easy_trails.iloc[0]['trail_name'],
                'name2': random_easy_trails.iloc[1]['trail_name'],
                'name3': random_easy_trails.iloc[2]['trail_name']
            }
        # Select 3 random trails for Intermediate
        elif result['hiking_experience'] == 'Intermediate':
            int_trails = data[data['intensity_rating'] == 'Moderate']
            random_int_trails = int_trails.sample(n=3, replace=True) if len(int_trails) >= 3 else int_trails
            st.session_state.trail_options = {
                'option1': random_int_trails.iloc[0],
                'option2': random_int_trails.iloc[1],
                'option3': random_int_trails.iloc[2],
                'name1': random_int_trails.iloc[0]['trail_name'],
                'name2': random_int_trails.iloc[1]['trail_name'],
                'name3': random_int_trails.iloc[2]['trail_name']
            }
        # # Select 3 random trails for Advanced
        elif result['hiking_experience'] == 'Advanced':
            diff_trails = data[data['intensity_rating'] == 'Challenging']
            random_diff_trails = diff_trails.sample(n=3, replace=True) if len(diff_trails) >= 3 else diff_trails
            st.session_state.trail_options = {
                'option1': random_diff_trails.iloc[0],
                'option2': random_diff_trails.iloc[1],
                'option3': random_diff_trails.iloc[2],
                'name1': random_diff_trails.iloc[0]['trail_name'],
                'name2': random_diff_trails.iloc[1]['trail_name'],
                'name3': random_diff_trails.iloc[2]['trail_name']
            }
    #Display the three random trails in buttons
    st.write("Here are some " + result['hiking_experience'] + " trails you can check out. Click one to learn more!")
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button(st.session_state.trail_options['name1'], key="button1", on_click=show_trail_details, args=(st.session_state.trail_options['option1'],)):
            pass
    with col2:
        if st.button(st.session_state.trail_options['name2'], key="button2", on_click=show_trail_details, args=(st.session_state.trail_options['option2'],)):
            pass
    with col3:
        if st.button(st.session_state.trail_options['name3'], key="button3", on_click=show_trail_details, args=(st.session_state.trail_options['option3'],)):
            pass

    # Display trail details using session state
    if st.session_state.show_details and st.session_state.selected_trail is not None:
        printDict = st.session_state.selected_trail
        st.write("")
        st.write("Trail Name: " + str(printDict["trail_name"]))
        st.write("Hike Length (miles): " + str(printDict["hike_length"]))
        st.write("Elevation Change (gain/loss): " + str(printDict["elevation_gain_loss"]))
        st.write("Intensity: " + str(printDict["intensity_rating"]))
        st.write("Decsription: " + str(printDict["Description"]))
        st.write("")
        st.write("Is this the trail you want to try?")
        # Create two columns for the buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes", key="confirm_trail"):
                st.session_state.selected_trail_name = printDict["trail_name"]
        with col2:
            # Refresh button to get new trail options
            if st.button("Refresh Options", key="refresh_trails"):
                st.session_state.trail_options = None
                st.session_state.selected_trail = None
                st.session_state.show_details = False
                st.session_state.selected_trail_name = None
                st.rerun()
    else:
        st.write("Pick a trail to learn more about...")
# Only show the map and additional information if a trail is selected
if st.session_state.selected_trail_name:
    #Location Map
    st.markdown("# Location Map")
    
    # Extract the first values from latitude and longitude columns
    selected_trail = data[data['trail_name'] == st.session_state.selected_trail_name]
    
    if not selected_trail.empty:
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
    
    # Plants and Terrain Prototype
    def get_completion2(model="gpt-3.5-turbo"):
        prompt = f"For the trail {st.session_state.selected_trail_name}, create exactly 9 items in this format:\n\
                  PLANTS:\n\
                  1. [plant 1]\n\
                  2. [plant 2]\n\
                  3. [plant 3]\n\
                  ANIMALS:\n\
                  1. [animal 1]\n\
                  2. [animal 2]\n\
                  3. [animal 3]\n\
                  TERRAIN:\n\
                  1. [terrain 1]\n\
                  2. [terrain 2]\n\
                  3. [terrain 3]\n\
                  \n\
                  Provide exactly one item per line, no extra text."
        
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert trail guide. Follow the exact format requested, with 3 items per category."},
                {"role": "user", "content": prompt},
            ]
        )
        return completion.choices[0].message.content

    def parse_table_content(text):
        # Initialize empty lists
        plants = []
        animals = []
        terrain = []
        current_category = None
        
        # Process the text line by line
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        for line in lines:
            if 'PLANTS:' in line:
                current_category = 'plants'
                continue
            elif 'ANIMALS:' in line:
                current_category = 'animals'
                continue
            elif 'TERRAIN:' in line:
                current_category = 'terrain'
                continue
                
            # Remove numbering if present
            if '. ' in line:
                line = line.split('. ')[1]
                
            if current_category == 'plants' and len(plants) < 3:
                plants.append(line)
            elif current_category == 'animals' and len(animals) < 3:
                animals.append(line)
            elif current_category == 'terrain' and len(terrain) < 3:
                terrain.append(line)
        
        # Ensure we have exactly 3 items per category
        while len(plants) < 3:
            plants.append("Common wildflowers")
        while len(animals) < 3:
            animals.append("Local wildlife")
        while len(terrain) < 3:
            terrain.append("Natural trail surface")
            
        return plants[:3], animals[:3], terrain[:3]

    def get_image(first_row_items, model="dall-e-2"):
        prompts = [
            f"Generate a realistic nature photograph of {first_row_items[0]} in its natural habitat, high quality nature photography style",
            f"Generate a realistic wildlife photograph of {first_row_items[1]} in its natural habitat, high quality wildlife photography style",
            f"Generate a realistic landscape photograph showing {first_row_items[2]}, high quality landscape photography style"
        ]
        
        all_urls = []
        for prompt in prompts:
            images = client.images.generate(
                prompt=prompt,
                model=model,
                n=1,
                size="1024x1024"
            )
            all_urls.append(images.data[0].url)
        return all_urls

    # If not ready add a spinner
    with st.spinner("Loading trail information..."):
        # Get and display table content
        table_content = get_completion2()
        plants, animals, terrain = parse_table_content(table_content)
        
        # Create and display the table
        st.subheader('Trail Information Table:', divider='grey')
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Plants**")
            for plant in plants:
                st.write(f"• {plant}")
                
        with col2:
            st.markdown("**Animals**")
            for animal in animals:
                st.write(f"• {animal}")
                
        with col3:
            st.markdown("**Terrain**")
            for terrain_type in terrain:
                st.write(f"• {terrain_type}")

        # Generate and display images based on first row
        first_row = [plants[0], animals[0], terrain[0]]
        urls = get_image(first_row)

        st.subheader('Visual Preview:', divider='grey')
        image_col1, image_col2, image_col3 = st.columns(3)

        with image_col1:
            st.header("Plants")
            st.image(urls[0], caption=plants[0], use_column_width=True)

        with image_col2:
            st.header("Animals")
            st.image(urls[1], caption=animals[0], use_column_width=True)

        with image_col3:
            st.header("Terrain")
            st.image(urls[2], caption=terrain[0], use_column_width=True)
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