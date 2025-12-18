import streamlit as st

st.set_page_config(
    page_title="Error",
    page_icon="⚠️",
    initial_sidebar_state="collapsed"
)


st.title("Oops! Something went wrong")
st.header("Your order has not been processed and you have not been charged")
st.header("Sorry, Please try again")
st.page_link("pages/products.py", label="Continue Shopping")