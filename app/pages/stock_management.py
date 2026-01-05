import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import iris
import io

# Define admin credentials 
# !! WARNING !! 
# Never hardcode credentials in production environments. 
DUMMY_USERNAME = "admin"
DUMMY_PASSWORD = "1234"

# Initialize session state for authentication (boolean) and uploader key
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0


# *********************************************************************************
# ****************************** FUNCTION DEFINITIONS ******************************

## Creates log-in form to authenticate the user as an administrator
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


def add_to_database(df:pd.DataFrame):
    '''
    Adds a dataframe to the database

    Workflow: 
        - Check that the schema matches the expected schema of the data table.
        - Queries the database to collect all of the existing product ids. 
        - splits the order dataframe by whether it is new or already in the database (requires inserting or updating) 
        - Updates the existing product stocks in the database
        - Inserts the new products into the database
    '''

    # Checks if the dataframe has the correct schema
    if set(df.columns) != {"ProductId", "Name", "Description", "CountryOfOrigin", "Price", "StockQuantity"}:
        print(df.columns)
        st.error("The dataframe provided does not match the database table schema", icon="🚨")
        st.warning("Data Not added")
        return -1
    
    with iris.connect("localhost", 1972, "USER", "SuperUser", "SYS") as conn:
        cursor = conn.cursor()

        # Get list of current product ids in the database 
        cursor.execute("SELECT ProductId FROM coffeeco.Inventory")
        current_ids = [x[0] for x in cursor.fetchall()]
        print(current_ids)

        # Split dataframe into existing products and new products
        existing_products_df = df[df["ProductId"].isin(current_ids)]
        new_products_df = df[~df["ProductId"].isin(current_ids)]

        if len(existing_products_df) > 0:

            update_query = f"""
                    UPDATE coffeeco.Inventory
                    SET StockQuantity = StockQuantity + ? 
                    WHERE ProductId = ?
                    """
            update_values = existing_products_df[["StockQuantity", "ProductId"]].values.tolist()
            cursor.executemany(update_query, update_values)
        
        if len(new_products_df)>0:

            insert_query = f"""INSERT INTO coffeeco.Inventory 
                        (ProductId, Name, Description, CountryOfOrigin, Price, StockQuantity) 
                        VALUES (?, ?, ?, ?, ?, ?)"""


            ## DELETE THESE TWO ROWS FOR CHALLENGE 03
            insert_list = new_products_df.values.tolist() 
            cursor.executemany(insert_query, insert_list)
        
        st.toast("Added data to database!")



def get_stock() -> pd.DataFrame:
    '''
    Retrieve the stock table in the dataframe
    '''

    # Define connection parameters and credentials
    server = "localhost"
    port = 1972
    namespace = "USER"

    ## ! Warning ! - don't hardcode credentials in production!
    username = "SuperUser"
    password = "SYS"

    # Create a connection string with the credentials
    db_url = f"iris://{username}:{password}@{server}:{port}/{namespace}"
    

    # Create SQLAlchemy Engine
    engine = create_engine(db_url)


    # SQL selection query to return all the stock
    sql =  """SELECT * FROM coffeeco.Inventory"""

    # Query DB with SQLAlchemy engine and Pandas to return a DataFrame 
    df = pd.read_sql(sql, engine)

    # Return the dataframe
    return df

# **********************************************************************************





# --------------------------- Main Page Creation -----------------------------------

# Show login form if unauthenticated
if False:
# if not st.session_state.authenticated:
    login_form()

# If authenticated, show rest of page
else:
    st.success("Authenticated")

    ## Create login button
    if st.button("Log out"):
        st.session_state.authenticated = False

    # Page headder
    st.header("View Stock")

    # Calls function to retrieve stock as a dataframe
    df = get_stock()

    # Displays current stock data
    st.dataframe(df)


    # Loading new stock 
    st.header("Load Stock CSV")
    st.write("Use the button below to load the stock CSV chart")


    ### Example using file upload (not possible in sandbox environment) 

    uploaded_csv = st.file_uploader("Load CSV", type="csv", key=f"uploader_{st.session_state.uploader_key}")
    # Activated upon file upload: 
    if uploaded_csv is not None: 
        #Read the csv file
        df = pd.read_csv(uploaded_csv)

        # csv_text = st.text_area("Paste CSV here", key=f"uploader_{st.session_state.uploader_key}")
        # if csv_text:
        #     df = pd.read_csv(io.StringIO(csv_text))

        # Display data in an editable format.
        df = st.data_editor(df)

        # Create a button to add the stock to the database
        if st.button("Add To Database"):
            # Calls the add_to_database function with the dataframe
            add_to_database(df)

            # Reset the file uploader once an order is uploaded to the database
            st.session_state.uploader_key += 1
            df = None

            # Refresh the page to see changes
            st.rerun() 
    

