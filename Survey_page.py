import streamlit as st
import time

st.markdown("# Survey 📑👩🏻‍💻📝")
st.sidebar.markdown("# Complete a quick survey for personalized plan!")

# Survey questions
hiking_before = st.radio(
    "Have you gone hiking before?",
    ["Yes", "No"],
    index=None,
)
st.write("You selected:", hiking_before)

hiking_experience = st.radio(
    "How would you rate your hiking experience?",
    ["Beginner", "Intermediate", "Advanced"],
    index=None,
)
st.write("You selected: ", hiking_experience)

weekly_exercise = st.radio(
    "How often do you exercise a week?",
    ["Not at all (None)", "Once a week (Light)", "2-3 Times a week (Moderate)", "4-5 Times a\
      week (Active)", "6-7 Times a week (Very Active)"],
    index=None,
)
st.write("You selected: ", weekly_exercise)

transportation = st.radio(
    "Do you have a form of transportation that lets you freely choose \
        where to park? (e.g. personal car, rental, or shared vehicle)",
    ["Yes", "No"],
    index=None,
)
st.write("You selected: ", transportation)

looking_for = st.radio(
    "What type of hike are you looking for?",
    ["Leisure", "Fitness", "Adventure", "Scenic Views"],
    index=None,
)
st.write("You selected: ", looking_for)

specific_features = st.radio(
    "Are you interested in hiking for specific features?",
    ["Waterfalls", "Lakes", "Forests", "Mountains"],
    index=None,
)
st.write("You selected: ", specific_features)

solo_or_group = st.radio(
    "Do you plan on hiking solo or in a group?",
    ["Solo", "Group"],
    index=None,
)
st.write("You selected: ", solo_or_group)

pet_on_trail = st.radio(
    "Do you plan on bringing a pet onto the trail?",
    ["Yes", "No"],
    index=None,
)
st.write("You selected: ", pet_on_trail)

disability_check = st.radio(
    "Are you interested in trails that are accessible to people with disabilities?",
    ["Yes", "No"],
    index=None,
)
st.write("You selected: ", disability_check)

time_check_start, time_check_end = st.select_slider(
    "Select a range for the length of your hiking experience: ",
    options=[
        "30 Minutes",
        "1 Hour",
        "2 Hours",
        "3 Hours",
        "4 Hours",
        "5 Hours",
        "6 Hours",
        "7 Hours",
        "8 Hours",
        "9 Hours",
        "10 Hours",
        "11 Hours",
        "12 Hours",
    ],
    value=("1 Hour", "2 Hours"),
)
st.write("You selected the range between", time_check_start, "and", time_check_end)

st.markdown('# Are you ready to go hiking?')
st.page_link("pages/Personalized_plan.py", label="Your Personalized Plan", icon="💡")