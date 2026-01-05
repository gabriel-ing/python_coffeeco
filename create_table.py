import iris

## Connection Parameters 
server = "localhost"
port = 1972
namespace = "USER"
username = "SuperUser"
password = "SYS"

## Create a connection
connection  = iris.connect(server, port, namespace, username, password)

## Create a Cursor
cursor = connection.cursor() 

## Drop table if it exists 
cursor.execute("DROP TABLE IF EXISTS coffeeco.Inventory ")


## SQL query to create a table 
create_table_query  = """CREATE TABLE coffeeco.Inventory ( 
    ProductId Integer NOT NULL PRIMARY KEY,
    Name VARCHAR(50), 
    Price DOUBLE, 
    StockQuantity Integer,
    CountryOfOrigin VARCHAR(50), 
    Description VARCHAR(500) 
    )"""

## Execute create table query
cursor.execute(create_table_query)

## Insert query
insert_query = """INSERT INTO coffeeco.Inventory 
                (ProductId, Name, Price, StockQuantity, CountryOfOrigin, Description)
                VALUES (?, ?, ?, ?, ?, ? )""" ## ? Is a placeholder for a value passed at runtime

## List of values to insert
values = [1001, "Colombian Supremo", 12.50, 5, "Colombia","Smooth and balanced with notes of chocolate and caramel."]

## Execute insertion
cursor.execute(insert_query, values) ## Values for ? placeholders passed in as a list