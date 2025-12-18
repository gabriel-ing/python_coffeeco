import streamlit as st



def main():
    """
    Function to generate navigation for the homepage.
    """
    pages = [st.Page("pages/homepage.py", title="Homepage", icon="☕"), 
                            st.Page("pages/products.py", title="Shop"), 
                            st.Page("pages/checkout.py", title="Checkout"),
                            st.Page("pages/stock_management.py", title="Manage databases"),
                            st.Page("pages/hidden/error.py", title="Error"),
                            st.Page("pages/hidden/thanks.py", title="thanks"),
                            #st.Page("pages/hidden/playground.py", title="Test-playground")
                            
                            ]    



    pg = st.navigation(pages, position="hidden")
    pg.run()
  
    st.sidebar.header("Python CoffeeCo")
    st.sidebar.page_link("pages/homepage.py", label="Home")
    st.sidebar.page_link("pages/products.py", label="Shop")
    st.sidebar.page_link("pages/checkout.py", label="Checkout")

    st.sidebar.header("Administration")
    st.sidebar.page_link("pages/stock_management.py", label="Manage Stock")
    
    #st.sidebar.page_link("pages/hidden/playground.py", label="dev")


if __name__ == "__main__":
    main()
    