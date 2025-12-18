import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import iris

# ---- Configuration: set your dummy credentials here ----
DUMMY_USERNAME = "admin"
DUMMY_PASSWORD = "1234"

# ---- Initialize session state ----
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login_form():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Log in", shortcut="Enter")

    if login_btn:
        if username == DUMMY_USERNAME and password == DUMMY_PASSWORD:
            st.session_state.authenticated = True
        else:
            st.error("Invalid username or password")

def logout_button():
    if st.button("Log out"):
        st.session_state.authenticated = False
        


def preview_data():
    
    df = pd.read_csv("../data/stock-data.csv")
    st.data_editor(df)




def add_to_database(df):
    insert_query = f"INSERT INTO coffeeco.Inventory (Name, Description, CountryOfOrigin, Price, StockQuantity) VALUES (?, ?, ? , ?, ?)"
    df_lists = df.values.tolist()

    conn = iris.connect("localhost", 1972, "USER", "SuperUser", "SYS")
    cursor = conn.cursor()
    print(df_lists)
    status = cursor.executemany(insert_query, df_lists)
    
    st.write("Added data to database!")


def get_stock() -> pd.DataFrame:

    server = "localhost"
    port = 1972
    namespace = "USER"
    username = "SuperUser"
    password = "SYS"

    db_url = f"iris://{username}:{password}@{server}:{port}/{namespace}"
    sql = """SELECT * FROM coffeeco.Inventory"""

    engine = create_engine(db_url)
    
    df = pd.read_sql(sql, engine)
    return df


# ---- App ----
if not st.session_state.authenticated:
    login_form()
else:
    st.success("Authenticated")
    logout_button()



    st.header("View Stock")

    df = get_stock()
    st.dataframe(df)

    st.header("Load Stock CSV")
    st.write("Use the button below to load the stock CSV chart")
    uploaded_file = st.file_uploader("Load CSV", type="csv")
    if uploaded_file is not None: 
        df = pd.read_csv(uploaded_file)
        df = st.data_editor(df)
        if st.button("Add To Database"):
            add_to_database(df)
            st.rerun() 
    

    # st.header("Add Data Manually")

    


    # editable_df = pd.DataFrame({
    #     "Name": pd.Series(dtype="string"),
    #     "Description": pd.Series(dtype="string"),
    #     "CountryOfOrigin": pd.Series(dtype="string"),
    #     "Price": pd.Series(dtype="float64"),
    #     "StockQuantity": pd.Series(dtype="Int64")  # pandas nullable int
    # })


    # editable_df = st.data_editor(editable_df,num_rows="dynamic")
    # if st.button("Add changes to DB"):
        
    #     add_to_database(editable_df)