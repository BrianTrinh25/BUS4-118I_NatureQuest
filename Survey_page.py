import streamlit as st
import streamlit_survey as ss

st.markdown("# Survey 📑👩🏻‍💻📝")
st.sidebar.markdown("# Complete a quick survey for personalized plan!")

survey = ss.StreamlitSurvey()
pages = survey.pages(8, on_submit=lambda: st.success("Your responses have been recorded. Thank you!"))
with pages:
    if pages.current == 0:
        st.write("Let's get started!")
    if pages.current == 1:
        st.write("Have you gone hiking before?")
        hiking_before = survey.radio(
            "hiking_before",
            options=["✅ Yes", "❌ No"],
            index=None,
            label_visibility="collapsed",
            horizontal=True,
        )
        if hiking_before == "✅ Yes":
            st.write("How would you rate your hiking experience?")
            hiking_experience = survey.radio(
                "hiking_before_yes",
                options=["Beginner", "Intermediate", "Advanced"],
                label_visibility="collapsed",
                index=None,
                horizontal = True,
            )
        elif hiking_before == "❌ No":
            st.write("That's okay to hear! Hope you're excited to go hiking!")
            hiking_experience = "Beginner"
    elif pages.current == 2:
        st.write("Do you have a form of transportation that lets you freely choose \
        where to park? (e.g. personal car, rental, or shared vehicle)")
        transportation = survey.radio(
            "transportation_check",
            options=["Yes", "No"],
            horizontal=True,
            label_visibility="collapsed"
        )
    elif pages.current == 3:
        st.write("Pick an option for a specific feature you might like to see on your hike: ")
        col1, col2, col3, col4 = st.columns([1,1,1,1])
        with col1:
            st.image("https://s.hdnux.com/photos/01/36/43/64/24788256/3/ratio3x2_1920.jpg", caption= None, use_column_width=True) 
            if st.button("Waterfalls", key="button1"):
                specific_features = "Waterfalls"
        with col2:
            st.image("https://alamedapost.com/wp-content/uploads/2024/09/DSC_1383_Resized-1024x683.jpg", caption= None, use_column_width=True) 
            if st.button("Lakes", key="button2"):
                specific_features = "Lakes"
        with col3:
            st.image("https://media.cntraveler.com/photos/65de1637b4f65c227f63206d/master/w_1600,c_limit/GettyImages-474009330.jpeg", caption= None, use_column_width=True) 
            if st.button("Forests", key="button3"):
                specific_features = "Forests"
        with col4:
            st.image("https://media.cntraveler.com/photos/6072054bac52332b71f172b3/master/w_1600,c_limit/DDCK8A.jpg", caption= None, use_column_width=True) 
            if st.button("Mountains", key="button4"):
                feature = "Mountains"
    elif pages.current == 4:
        st.write("Are you looking for a solo hike or hike in a group?")
        col1, col2, = st.columns([1,1])
        solo_or_group = "None"
        with col1:
            if st.button("Solo", key="button1"):
                solo_or_group = "Solo"
        with col2:
            if st.button("Group", key="button2"):
                solo_or_group = "Group"
    elif pages.current == 5:
        st.write("Do you plan on bringing a pet onto the trail?")
        pet_on_trail = survey.radio(
            "pet_check",
            options=["Yes", "No"],
            horizontal=True,
            label_visibility="collapsed"
        )
    elif pages.current == 6:
        st.write("Are you interested in trails that are accessible to people with disabilities?")
        disability_check = survey.radio(
            "disability_check",
            options=["Yes", "No"],
            horizontal=True,
            label_visibility="collapsed"
        )
    elif pages.current == 7:
        time_check_start, time_check_end = st.select_slider(
        "Select a range for the length of your hiking experience: ",
            options=["30 Minutes","1 Hour","2 Hours","3 Hours","4 Hours","5 Hours","6 Hours","7 Hours",
        "8 Hours","9 Hours","10 Hours","11 Hours","12 Hours",
    ],
        value=("1 Hour", "2 Hours")
    )  
        st.markdown('# Are you ready to go hiking?')
        st.page_link("pages/Personalized_plan.py", label="Your Personalized Plan", icon="💡")
        
my_bar = st.progress(int(pages.current*100/7), "Question " + str(pages.current) + " out of 7")
