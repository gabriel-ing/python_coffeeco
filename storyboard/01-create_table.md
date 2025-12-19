# Create the data table

The InterSystems IRIS data platforms is many things. It is an engine for linking operations through interopability productions. It is an analytics platform. It is a powerful tool for machine learning and AI, through its integrated ML platform and vector search capabilitys.

However, at its core, InterSystems IRIS is a very fast database.

In this tutorial we are going to explore how InterSystems IRIS can be used as a classic back-end database for an online shop, using pure Python. Unlike other tutorials, this tutorial will not show any InterSystems IRIS interface, but instead, it will show how InterSystems IRIS can be accessed by Python code.

Lets begin by creating the data table. Here will will connect to our running instance of InterSystems IRIS by the intersystems DB-API, which can be easily installed with pip (`pip install intersystems-irispython`). 

In the terminal window, start an interactive python shell:

```nocopy,run,line-numbers
python
```

Now, in this interactive shell, we can create a connection to InterSystems IRIS.

```nocopy,run,line-numbers
import iris

server = "iris" # IRIS container running on the local network 
port = 1972 # Binary superserver connection port
namespace = "USER" # Default namespace
username = "SuperUser" # Default Username
password = "SYS" # Default Password

connection = iris.connect(server, port, namespace, username, password)
```

> [!IMPORTANT]
> In production, these values should be changed from the defaults and hidden!

We then can create a cursor object, which can execute commands using the `.execute()` method.

```nocopy, run, line-numbers
cursor = connection.cursor()

# Test a simple SQL queries
cursor.execute("SELECT 1+1")
# Extract the row and value 
value = cursor.fetchone()[0]
# Print the value
print(value)
```

The terminal should print 2. Great! Now lets create a table for our Inventory. Run the following, this is a standard SQL query to create a table with the schema given. 

```nocopy,run,line-numbers
# SQL query to create a table 
create_table_query  = """CREATE TABLE coffeeco.Inventory ( 
    Name VARCHAR(50), 
    Price DOUBLE, 
    StockQuantity Integer,
    CountryOfOrigin VARCHAR(50), 
    Description VARCHAR(500) 
    )"""

# Execute the query
cursor.execute(create_table_query)
```


Finally, lets add a single row of data. Here we will define an insert query, with placeholders for each value. Then, we execute the query, adding a list of the values as parameters. 

```nocopy,run,line-numbers
# Insert query
insert_query = """INSERT INTO coffeeco.Inventory 
                (Name, Price, StockQuantity, CountryOfOrigin, Description)
                VALUES (?, ?, ?, ?, ? )""" # ? Is a placeholder for a value passed at runtime

# List of values to insert
values = [
        "Colombian Supremo", # Name  
        12.50, # Price
        5, # Stock Quantity
        "Colombia", # Country of origin
        "Smooth and balanced with notes of chocolate and caramel." # Description
    ]

# Execute insertion
cursor.execute(insert_query, values) ## Values for ? placeholders passed in as a list
```

Great, lets just double check it has been added: 

```nocopy,run,line-numbers
# Execute SELECT query
cursor.execute("SELECT * FROM coffeeco.Inventory)

# Return the values
rows = cursor.fetchall()

# print the values
print(rows)
```