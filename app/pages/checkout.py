import streamlit as st
import pandas as pd
import time 
import iris

st.title("Checkout")


def update_database(id:int):
    # Open Product Object by ID
    item = irispy.classMethodObject("coffeeco.Inventory", "%OpenId", id)

    # Check if all stock is being bought
    if st.session_state.basket[id]["Quantity"] == item.get("StockQuantity"):
                
        # Send internal alert from the server using pre-written method
        status = irispy.classMethodString("coffeeco.Alerts", "OutOfStockAlert", id, item.get("Name"))
                
        # Delete the item from the database
        irispy.classMethodVoid("coffeeco.Inventory", "%DeleteId", id)
            
    else: # The item is not sold out
                
        # Calculate the new quantity in stock
        new_quantity = item.get("StockQuantity") - st.session_state.basket[id]["Quantity"]
                
        # Send alert if stock is low
        if new_quantity<3:
            status = irispy.classMethodString("coffeeco.alerts", "LowStockAlert", id, item.get("Name"))
                
        # Update the quantity in stock
        item.set("StockQuantity", new_quantity) 
                
        # Save the item
        item.invokeVoid("%Save")



# Create page saying basket is empty
if "basket" not in st.session_state or st.session_state.basket=={}:
    st.subheader("Basket currently empty...")
    st.page_link("pages/products.py", label="Continue Shopping")


# If basket is not empty, create checkout page
else:
    print(st.session_state.basket)
    
    # Create a Pandas Dataframe from the basket dictionary
    basket = (
        pd.DataFrame.from_dict(st.session_state.basket, orient='index')
        .reset_index()
        .rename(columns={'index': 'id'})
        [['id', 'Name', 'Price', 'Quantity']]
    )
    
    # Set number display to two decimal places
    pd.set_option("display.precision", 2)

    # Create subtotal column 
    basket["Subtotal"] = basket["Price"]*basket["Quantity"]

    # Calculate totals
    total_quantity = basket["Quantity"].sum()
    total = basket["Subtotal"].sum()

    basket["Subtotal"] = "$ " + basket["Subtotal"].round(2).astype(str)

    # Write Itemised list of basket
    st.header("Items")
    table = st.table(basket)

    # Add slight delay for calculating. Unneccessary but looks satisfying...
    time.sleep(0.5)

    st.header("Total")

    # Create table of subtotals and totals
    total_row = pd.DataFrame([[ f"{total_quantity} items", f"$ {(total-0.2*total).round(2)}", f"$ {(0.2*total).round(2)}",  f"$ {total.round(2)}"]],
                            columns=["Quantity", "Subtotal", "Tax","Total"])

    # Style the table
    styled_total = total_row.style.set_properties(**{
        "font-weight": "bold",
        "text-align": "right"
    }).set_table_styles([
        {"selector": "th", "props": [("text-align", "right")]}
    ])

    # Show table with the total 
    st.table(styled_total)

    

    # Create the button with an on-click function
    if st.button("Pay Now!"):

        with iris.connect(iris.connect("localhost", 1972, "USER", "SuperUser", "SYS")) as connection:
            irispy = iris.createIRIS(connection)

            # Iterate over products in basket
            for id in st.session_state.basket:
                
                # Call the function to update the database
                update_database(id)

            # Reset basket
            st.session_state.basket = {}
            
            # Redirect user to confirmation page
            st.switch_page( "pages/hidden/thanks.py")
