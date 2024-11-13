import streamlit as st
import streamlit_survey as ss

#format sidebar
st.markdown("""
    <style>
      section[data-testid="stSidebar"] {
        top: -7%; 
        height: 200% !important;
        background-color: #E3FFD5;
      }
    </style>""", unsafe_allow_html=True)
st.sidebar.image("pages/logo.png", use_column_width=True, caption=None)

st.markdown("# Survey 📑👩🏻‍💻📝")
st.sidebar.markdown("# Complete a quick survey for personalized plan!")

#create results checker
result = st.session_state
if 'hiking_before' not in result:
    result['hiking_before'] = ""
if 'hiking_experience' not in result:
    result['hiking_experience'] = ""
if 'specific_features' not in result:
    result['specific_features'] = ""
if 'pet_on_trail' not in result:
    result['pet_on_trail'] = ""
if 'disability_check' not in result:
    result['disability_check'] = ""
if 'time_check_start' not in result:
    result['time_check_start'] = ""
if 'time_check_end' not in result:
    result['time_check_end'] = ""

survey = ss.StreamlitSurvey()

#survey
pages = survey.pages(6, on_submit=lambda: st.switch_page("pages/transition.py"))
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
            horizontal=True                
        )
        result["hiking_before"] = hiking_before
        if hiking_before == "✅ Yes":
            st.write("How would you rate your hiking experience?")
            hiking_experience = survey.radio(
                "hiking_before_yes",
                options=["Beginner", "Intermediate", "Advanced"],
                label_visibility="collapsed",
                index=None,
                horizontal = True,
            )
            result["hiking_experience"] = hiking_experience
        elif hiking_before == "❌ No":
            st.write("That's okay to hear! Hope you're excited to go hiking!")
            hiking_experience = "Beginner"
            result["hiking_experience"] = hiking_experience
    elif pages.current == 2:
        st.write("Pick an option for a specific feature you might like to see on your hike: ")
        col1, col2, col3, col4 = st.columns([1,1,1,1])
        with col1:
            st.image("https://s.hdnux.com/photos/01/36/43/64/24788256/3/ratio3x2_1920.jpg", caption= None, use_column_width=True) 
            if st.button("Waterfalls", key="button1"):
                result["specific_features"] = "Waterfalls"
        with col2:
            st.image("https://alamedapost.com/wp-content/uploads/2024/09/DSC_1383_Resized-1024x683.jpg", caption= None, use_column_width=True) 
            if st.button("Lakes", key="button2"):
                result["specific_features"] = "Lakes"
        with col3:
            st.image("https://media.cntraveler.com/photos/65de1637b4f65c227f63206d/master/w_1600,c_limit/GettyImages-474009330.jpeg", caption= None, use_column_width=True) 
            if st.button("Forests", key="button3"):
                result["specific_features"] = "Forests"
        with col4:
            st.image("https://media.cntraveler.com/photos/6072054bac52332b71f172b3/master/w_1600,c_limit/DDCK8A.jpg", caption= None, use_column_width=True) 
            if st.button("Mountains", key="button4"):
                result["specific_features"] = "Mountains"
    elif pages.current == 3:
        st.write("Do you plan on bringing a pet onto the trail?")
        pet_on_trail = survey.radio(
            "pet_check",
            options=["Yes", "No"],
            horizontal=True,
            index=None,
            label_visibility="collapsed"
        )
        result["pet_on_trail"] = pet_on_trail
    elif pages.current == 4:
        st.write("Are you interested in trails that are accessible to people with disabilities?")
        disability_check = survey.radio(
            "disability_check",
            options=["Yes", "No"],
            horizontal=True,
            index=None,
            label_visibility="collapsed",
            
        )
        result["disability_check"] = disability_check
    elif pages.current == 5:
        time_check_start, time_check_end = st.select_slider(
        "Select a range for the length of your hiking experience: ",
            options=["30 Minutes","1 Hour","2 Hours","3 Hours","4 Hours","5 Hours","6 Hours","7 Hours",
        "8 Hours","9 Hours","10 Hours","11 Hours","12 Hours",
    ],
        value=("1 Hour", "2 Hours")
    ) 
        result["time_check_start"] = time_check_start
        result["time_check_end"] = time_check_end
        
#progress bar
my_bar = st.progress(int(pages.current*100/5), "Question " + str(pages.current) + " out of 5")