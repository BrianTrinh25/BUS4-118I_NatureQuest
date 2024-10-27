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
    'lat': [37.307226530422035, 37.269817968115234, 37.445452198845956, 37.42591903699686, 37.3954045204858, 37.293801584395865, 37.23301521261931],
    'lon': [-121.9137624590682, -121.94942483361638, -121.84741556130625, -121.92485823400975, -121.82525695742902, -122.04148682149903, -121.92715082443866]
})

# Plot the map with the updated DataFrame
st.map(df)