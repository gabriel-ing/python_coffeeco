import streamlit as st
import pandas as pd

st.title("Welcome To PythonCoffeeCo! ")
st.header("The only Independent Coffee Roasters On Snake Island")

st.subheader("Visit our shop!")
st.page_link("pages/products.py", label="Shop", width="stretch", )

st.subheader("Our Branches")
df = pd.DataFrame([{"LON":-46.67460623020751, "LAT":-24.485781323765877},
                    {"LON":-46.67489, "LAT":-24.48099},
                    {"LON":-46.6760, "LAT":-24.48019}])
st.map(df, size=10, zoom=12)

