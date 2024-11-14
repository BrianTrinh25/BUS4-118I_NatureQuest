import os
import openai
import streamlit as st
import time
from openai import OpenAI
import pandas as pd
from Survey_page import result


# Initialize session state if nonexisting
if 'selectedTrail' not in st.session_state:
    st.session_state.selectedTrail = None
if 'showDetails' not in st.session_state:
    st.session_state.showDetails = False
if 'trailOptions' not in st.session_state:
    st.session_state.trailOptions = None
if 'selectedTrailName' not in st.session_state:
    st.session_state.selectedTrailName = None

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
st.sidebar.markdown("# Your personalized plan begins here.")
st.markdown("# Trail Selection")
# Load the dataset into a pandas DataFrame
data = pd.read_excel('pages/trail_list.xlsx')

learnMoreOption = ""
trail_selection = ""

# Define callback functions for buttons
def show_trail_details(trail_option):
    st.session_state.selectedTrail = trail_option
    st.session_state.showDetails = True

#Trail Selection
st.success("Here we go! Let's go outside!")
with st.spinner("That's great to know! Here are some hikes you can go on"):
    if st.session_state.trailOptions is None:
        # Select 3 random trails for Beginner
        if result['hiking_experience'] == 'Beginner':
            easy_trails = data[data['intensity_rating'] == 'Easy']
            random_easy_trails = easy_trails.sample(n=3, replace=True) if len(easy_trails) >= 3 else easy_trails
            st.session_state.trailOptions = {
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
            st.session_state.trailOptions = {
                'option1': random_int_trails.iloc[0],
                'option2': random_int_trails.iloc[1],
                'option3': random_int_trails.iloc[2],
                'name1': random_int_trails.iloc[0]['trail_name'],
                'name2': random_int_trails.iloc[1]['trail_name'],
                'name3': random_int_trails.iloc[2]['trail_name']
            }
        # Select 3 random trails for Advanced
        elif result['hiking_experience'] == 'Advanced':
            diff_trails = data[data['intensity_rating'] == 'Challenging']
            random_diff_trails = diff_trails.sample(n=3, replace=True) if len(diff_trails) >= 3 else diff_trails
            st.session_state.trailOptions = {
                'option1': random_diff_trails.iloc[0],
                'option2': random_diff_trails.iloc[1],
                'option3': random_diff_trails.iloc[2],
                'name1': random_diff_trails.iloc[0]['trail_name'],
                'name2': random_diff_trails.iloc[1]['trail_name'],
                'name3': random_diff_trails.iloc[2]['trail_name']
            }
    # Display the three random trails in buttons
    st.write("Here are some " + result['hiking_experience'] + " difficulty trails you can check out. Click one to learn more!")
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button(st.session_state.trailOptions['name1'], key="button1", on_click=show_trail_details, args=(st.session_state.trailOptions['option1'],)):
            pass
    with col2:
        if st.button(st.session_state.trailOptions['name2'], key="button2", on_click=show_trail_details, args=(st.session_state.trailOptions['option2'],)):
            pass
    with col3:
        if st.button(st.session_state.trailOptions['name3'], key="button3", on_click=show_trail_details, args=(st.session_state.trailOptions['option3'],)):
            pass

    # Display trail details if button clicked
    if st.session_state.showDetails and st.session_state.selectedTrail is not None:
        printDict = st.session_state.selectedTrail
        st.write("")
        st.write("Trail Name: " + str(printDict["trail_name"]))
        st.write("Hike Length (miles): " + str(printDict["hike_length"]))
        st.write("Elevation Change (gain/loss): " + str(printDict["elevation_gain_loss"]))
        st.write("Intensity: " + str(printDict["intensity_rating"]))
        st.write("Description: " + str(printDict["Description"]))
        st.write("")
        st.write("More information will appear in the sidebar and on this page after confirming your trail!")
        st.write("")
        st.write("Is this the trail you want to try?")
        # Create two columns for the buttons
        col1, col2 = st.columns(2)
        with col1:
            # Yes button
            if st.button("Yes", key="confirm_trail"):
                st.session_state.selectedTrailName = printDict["trail_name"]
        with col2:
            # Refresh button to get new trail options
            if st.button("Refresh Options", key="refresh_trails"):
                st.session_state.trailOptions = None
                st.session_state.selectedTrail = None
                st.session_state.showDetails = False
                st.session_state.selectedTrailName = None
                st.rerun()
    else:
        st.write("Pick a trail to learn more about...")
# Only show the map and additional information if Yes button clicked
if st.session_state.selectedTrailName:
    st.sidebar.page_link("pages/Personalized_plan.py", label="Personalized Plan")
    st.sidebar.page_link("pages/packinginfo.py", label = "Packing Info")
    st.sidebar.page_link("pages/educationplan.py", label = "Education Plan")
    result['selected_trail'] = st.session_state.selectedTrailName
    #Location Map
    st.markdown("# Location Map")
    
    # Extract the first values from latitude and longitude columns
    selectedTrail = data[data['trail_name'] == st.session_state.selectedTrailName]
    
    if not selectedTrail.empty:
        # Extract the first values from latitude and longitude columns
        lat = selectedTrail['latitude'].iloc[0]
        lon = selectedTrail['longitude'].iloc[0]

        # Update the DataFrame with the specific coordinates
        df = pd.DataFrame({
            'lat': [lat],
            'lon': [lon]
        })

        # Plot the map with the updated DataFrame
        st.map(df)
    
    # Plants and Terrain Prototype
    def get_completion2(model="gpt-3.5-turbo"):
        prompt = f"For the trail {st.session_state.selectedTrailName}, create exactly 9 items in this format:\n\
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
        # Make an empty list for each of the topics
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
    with st.spinner("Loading more information..."):
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

        st.subheader('AI Generated Preview:', divider='grey')
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