import streamlit as st
import pandas as pd

st.markdown("# Hiking Map Prototype")
st.sidebar.markdown("# Hiking Map Prototype")

zip = st.number_input(
    "Zip code", value=None, placeholder="Zip Code"
)

distance = st.selectbox(
    "Distance",
    ("5 mi", "10 mi", "25 mi", "50 mi"),
)

# Update your DataFrame with the specific coordinates
df = pd.DataFrame({
    'lat': [37.307226530422035],
    'lon': [-121.9137624590682]
})

# Plot the map with the updated DataFrame
st.map(df)