import iris
import streamlit as st



if "basket" not in st.session_state:
    st.session_state.basket = {}  # {product_id: {"name": str, "qty": int, "price": float}}


def add_to_basket(id:int, name:str,price: float, quantity:int):
    if id in st.session_state.basket:
        st.session_state.basket[id]["quantity"]+=quantity
    else:
        st.session_state.basket[id] = {"Name": name, "Price":price, "Quantity":quantity }

    print(st.session_state.basket)


conn = iris.connect("localhost", 1972, "USER", "SuperUser", "SYS")
cursor = conn.cursor() 

cursor.execute("SELECT ID from coffeeco.Inventory")
ids = cursor.fetchall()
ids = [x[0] for x in ids] 
irispy = iris.createIRIS(conn)

# Define custom CSS for the container
st.markdown(
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

.custom-container div[data-testid="stContainer"] {
color:black;
border-radius: 10px;
overflow: scroll;
padding:5px;
margin: 10px 0px;
height: 300px;
width: 230px;
}
</style>
""",
unsafe_allow_html=True,
)




cols = st.columns(3, gap="small", border=False)

def write_column(i, id, item):
    col = i % 3
    container_class = "odd" if ((col) %2) else "even"

    with cols[col]:
        st.markdown(f'<div class="custom-container {container_class}">', unsafe_allow_html=True)

        with st.container(height=500):

            ## Retrieve product name
            st.header(item.get("Name"))

            ## Retrieve other product items
            st.subheader(f"Origin: {item.get("CountryOfOrigin")}")
            st.write(item.get("Description"))
            st.write(f"Price: {item.get("Price")}")
            
            try:
                ## Create a value for the quantity to add to basket
                ## Note the max value is the current quantity
                quantity = st.number_input("Quantity: ", value=1, max_value=item.get("StockQuantity"), key=f"input{id}")
            except Exception as e:
                print(e)
            
            ## Add a button to handle adding to the basket
            if st.button("Add To Basket", key=id):
                ## Call add to basket function 
                add_to_basket(id, item.get("Name"), item.get("Price"), quantity)
                st.toast('Added to Basket', icon="🧺")
                

        st.markdown("</div>", unsafe_allow_html=True)

# def write_column2(i, item):
#     with cols[i % 3]:

#         container_class = "odd" if i%2 else "even"

#         st.markdown(f"""
#         <div class= "custom-container {container_class}" >
#             <h3>{item.get("Name")}</h1>
#             <h4>Origin: {item.get("CountryOfOrigin")}</h2>
#             <p>{item.get("Description")}</p>
#             <h4> Price: {item.get("Price")}</h3>
#         <div>
#         """, unsafe_allow_html=True)

i = 1
## Iterate over product IDs
for id in ids:
    try:
        ## Open the object by ID
        item = irispy.classMethodObject("coffeeco.Inventory", "%OpenId", id)

        ## Write the column for the product number, ID and Object 
        write_column(i,id, item)
        i+=1
    except Exception as e: 
        break


