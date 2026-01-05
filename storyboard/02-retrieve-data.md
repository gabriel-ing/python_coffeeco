# Retrieving data via Streamlit

Now lets work on the front-end. We are using Streamlit, a highly simplified front-end development framework written in Python. While other frameworks are better for customisability, few can match Streamlit for ease with which one can create sleek webpages.

Of course, the methods for connecting to and using InterSystems IRIS shown here can be used with any Python framework, so if you feel more comfortable with Flask, Django or Reflux feel free!

## Start the app

The main application file is `main.py`. The way this website is implemented, the main.py file does not create a page in itself, but starts the application and initialises the navigation and side bar properties. Lets run this file to start the application. 

Feel free to read through this file to confirm that there is little of interest. Then when you are ready, switch to the `terminal` tab. To start the application:

```run,nocopy,
streamlit run main.py --server.port 8080
```

After a couple of seconds, your site should be active. Switch to the `CoffeeCo` tab to see the site homepage.

Not too bad right? Not going to win any design awards, but considering the page is built in less than 15 lines of code, it will do.

### Stock Management

We haven't built the products page yet, so lets not see whats there quite yet. First, lets make sure the stock is up to date.

Open the `Stock Management` page from the sidebar. You'll be prompted for log-in details. Luckily no-one has changed these from the default yet, so the log in is currently:

- Username: admin
- Password: 1234

If you were to take a look at the stock_management.py page, you'd see these credentials hard-coded in at the moment. Hopefully, it doesn't need stating not to do this. Never hard-code the password in production... (and, for what its worth, 1234 isn't a very secure password either...)

Once you've logged in, you will see an error message. We are trying to view the current stock but something at the moment there is a problem with the code. Lets take a look how we are retrieving this data. Open the code editor tab, then navigate to the file "app/pages/stock_management.py".

The file is structured with state definitions at the top, followed by function definitions, then the main application logic at the bottom. Let's start by scrolling to the bottom of the page (line 142) to find where we display the stock data.

```python
    # Calls function to retrieve stock as a dataframe
    df = get_stock()

    # Displays current stock data
    st.dataframe(df)
```

This looks fine - we are displaying the data with ` st.dataframe(df)`, which shows a dataframe as an interactive table in streamlit. The problem is probably how we are retrieving the data. Scroll to line 90 where the `get_stock` function is defined.

This function retrives data from the database using SQLAlchemy (note, we need to have the additional `sqlalchemy-iris` package installed for this). The basic set-up is as follows:

```python
from sqlachemy import create_engine
import pandas as pd

# Create a connection string with the iris credentials
db_url = f"iris://{username}:{password}@{server}:{port}/{namespace}"

# Create Engine
engine = create_engine(db_url)

# Define SQL query
sql_query = "SELECT ... FROM ..."

# Run SQL using Pandas read_sql
df = pd.read_sql(sql, engine)
```

So take a look at the code in the `get_stock()` function. What is missing?

We haven't written the SQL query!

Try writing a simple SQL query to retrieve _all the data_ from the _coffeeco.Inventory_ table. (Solution at the end of the page)

### See reults

Save the file and return to the application tab. Refresh the page, re-enter the credentials (admin / 1234) and (hopefully) take a look at our data! 

If successful, move on to the next challenge - uploading data. Otherwise, take a look at the solution below and try again

#### Solution

To fix the data retrieval, we need to provide a SQL query to call. To do so, change the line:
```python
sql = ""
```

to:

```python
sql = "SELECT * FROM coffeeco.Inventory"
```