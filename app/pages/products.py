import iris
import streamlit as st


st.page_link("pages/checkout.py",label="Checkout", width="stretch")

## Intialise basket
if "basket" not in st.session_state:
    st.session_state.basket = {}  # {product_id: {"Name": str, "Quantity": int, "Price": float}}


def write_product_tile(i, id, item):
    """
    Handle adding tile for each item
    """
    col = (i % 3) - 1
    container_class = "odd" if (i %2) else "even"

    with cols[col]:

        ## Adds a mini html container for design (adds a strip of color)
        st.html(f'<div class="{container_class}">')

        with st.container(height=550):

            ## Retrieve product name
            st.header(item.get("Name"))

            ## Write other product properties
            st.subheader(f"Origin: {item.get("CountryOfOrigin")}")
            st.write(item.get("Description"))
            st.subheader(f"$ {item.get("Price")}")
            
            
            ## Set a trackable state for the max quantity
            ## so it can be dynamically updated with the basket
            if f"max_qty{id}" not in st.session_state:
                st.session_state[f"max_qty{id}"] = item.get("StockQuantity")

            
             ## Create an input for the quantity to add to basket
            quantity = st.number_input("Quantity: ",max_value=st.session_state[f"max_qty{id}"], key=f"input{id}")

            
            ## Add a button to handle adding to the basket
            st.button("Add To Basket", key=id,
                       on_click=lambda:\
                        add_to_basket(id, item.get("Name"), item.get("Price"), quantity))
                

def add_to_basket(id:int, name:str,price: float, quantity:int):
    """
    Function to handle adding an order to basket. 
    """

    # Checks if its already in basket - if so, update quantity
    if id in st.session_state.basket:
        st.session_state.basket[id]["Quantity"]+=quantity

    ## otherwise adds it to basket
    else:
        st.session_state.basket[id] = {"Name": name, "Price":price, "Quantity":quantity }

    ## prints current basket to terminal (debugging)
    print(st.session_state.basket)

    ## Resets quantity input and maximum quantity that can be purchased
    st.session_state[f"input{id}"] = 0
    st.session_state[f"max_qty{id}"] -= quantity

    ## Creates a toast pop-up to confirm added to basket
    st.toast('Added to Basket', icon="🧺")


# Define custom CSS for the container (formatting)
st.html(
"""
<style>

.odd{
background-color: #b2afe9; /* Light blue */
border: 2px solid #2F2A95; /* Steel blue border */
}
.even{
background-color: #99fffa; /* Light blue */
border: 2px solid #00B2A9; /* Steel blue border */
}


</style>
"""
)


## ****************************** IRIS Connection *****************

## IRIS connection
conn = iris.connect("localhost", 1972, "USER", "SuperUser", "SYS")
cursor = conn.cursor() 

## Fetch IDs in our dataset
cursor.execute("SELECT ID from coffeeco.Inventory")
ids = cursor.fetchall()
ids = [x[0] for x in ids]
cursor.close()

## Create IRIS native connection
irispy = iris.createIRIS(conn)


## Creates Columns
cols = st.columns(3, gap="small", border=False)


i = 1
## Iterate over product IDs
for id in ids:
    try:
        ## Open the object by ID
        item = irispy.classMethodObject("coffeeco.Inventory", "%OpenId", id)
        ## Write the column for the product number, ID and Object 
        write_product_tile(i,id, item)
        i+=1
    except Exception as e: 
        print(e)
        break


