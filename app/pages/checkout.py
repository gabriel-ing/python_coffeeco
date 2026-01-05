import streamlit as st
import pandas as pd
import time 
import iris

st.title("Checkout")

if "basket" not in st.session_state or st.session_state.basket=={}:
    st.subheader("Basket currently empty...")
    st.page_link("pages/products.py", label="Continue Shopping")


else:
    print(st.session_state.basket)
    basket = (
        pd.DataFrame.from_dict(st.session_state.basket, orient='index')
        .reset_index()
        .rename(columns={'index': 'id'})
        [['id', 'Name', 'Price', 'Quantity']]
    )

    pd.set_option("display.precision", 2)

    basket["Subtotal"] = basket["Price"]*basket["Quantity"]

    total_quantity = basket["Quantity"].sum()
    total = basket["Subtotal"].sum()
    basket["Subtotal"] = "$ " + basket["Subtotal"].round(2).astype(str)


    st.header("Items")
    table = st.table(basket)

    # Add slight delay for calculating... unneccessary but looks satisfying
    time.sleep(0.5)

    st.header("Total")
    # Example total row
    total_row = pd.DataFrame([["Total", f"{total_quantity} items", f"$ {(total-0.2*total).round(2)}", f"$ {(0.2*total).round(2)}",  f"$ {total.round(2)}"]],
                            columns=["Item", "Quantity", "Subtotal", "Tax","Total"])

    # Use style to format
    styled_total = total_row.style.set_properties(**{
        "font-weight": "bold",
        "text-align": "right"
    }).set_table_styles([
        {"selector": "th", "props": [("text-align", "right")]}
    ])

    st.table(styled_total)

    connection = iris.connect("localhost", 1972, "USER", "SuperUser", "SYS")
    irispy = iris.createIRIS(connection)

    if st.button("Pay Now!"):
        for id in st.session_state.basket:
            item = irispy.classMethodObject("coffeeco.Inventory", "%OpenId", id)

            if not item:
                st.switch_page("pages/hidden/error.py")
                break

            if st.session_state.basket[id]["Quantity"] == item.get("StockQuantity"):
                irispy.classMethodVoid("coffeeco.Inventory", "%DeleteId", id)
            else:
                new_quantity = item.get("StockQuantity") - st.session_state.basket[id]["Quantity"]
                item.set("StockQuantity", new_quantity) 
                item.invokeVoid("%Save")

        st.session_state.basket = {}
        st.switch_page( "pages/hidden/thanks.py")
