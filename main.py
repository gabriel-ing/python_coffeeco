import streamlit as st



def main():
    """
    Function to generate navigation for the homepage.
    """
    pages = [st.Page("pages/homepage.py", title="Homepage", icon="☕"), 
                            st.Page("pages/products.py", title="Shop"), 
                            st.Page("pages/checkout.py", title="Checkout"),
                            st.Page("pages/stock_management.py", title="Manage databases"),
                            st.Page("pages/error.py", title="Error"),
                            st.Page("pages/thanks.py", title="thanks")]    



    pg = st.navigation(pages, position="hidden")
    # hidden = st.navigation(hidden_pages, position="hidden")
    pg.run()
    # hidden.run()
    st.sidebar.header("Python CoffeeCo")
    st.sidebar.page_link("pages/homepage.py", label="Home")
    st.sidebar.page_link("pages/products.py", label="Shop")
    st.sidebar.page_link("pages/checkout.py", label="Checkout")

    st.sidebar.header("Administration")
    st.sidebar.page_link("pages/stock_management.py", label="Manage Stock")
    
    


if __name__ == "__main__":
    main()
    