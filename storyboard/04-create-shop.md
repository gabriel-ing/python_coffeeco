# Creating the shop page

Now we have the stock table, we need to create a page to display the products of our online store.

> [!NOTE]
> As mentioned before, Streamlit is known for its ease of use, not it's design customisability!
> For better looking designs, consider using another tool which includes HTML/CSS templates (e.g. Flask)

## Creating the product tiles

We want the shop to have a 'tile' with the product information for each product. We obviously don't want to manually create this for each product, so we can iterate over each product to create the tiles. 

While we could do this whole process using SQL queries, we are going to use an Object model, connecting to IRIS using a native connection. This will show how different data models can be combined and used in conjunction. This multi-modality is one of many things that sets InterSystems IRIS apart as a unique database and data-platform.

To create the product tiles, we need to do the following:

    - Collect the Product IDs 
    - Iterate over each product, and open the item as an object
    - Create a tile for each object using the properties of the object

Luckily some of this is already implemented: 

Collecting the product IDs using SQL:

```python
conn = iris.connect("localhost", 1972, "USER", "SuperUser", "SYS")
cursor = conn.cursor() 
## Fetch IDs in our dataset
cursor.execute("SELECT ID from coffeeco.Inventory")
ids = cursor.fetchall()
ids = [x[0] for x in ids]
cursor.close()
```
Creating the native connection: 

```python
## Create IRIS native connection
irispy = iris.createIRIS(conn)
```

Opening a product object for each product ID:
 (Code for generating the layout has been omitted)
```python
for id in ids:
        ## Open the object by ID
        item = irispy.classMethodObject("coffeeco.Inventory", "%OpenId", id)

        ## Write the column for the product number, ID and Object 
        write_product_tile(i,id, item)
```

> [!NOTE]
> This challenge focusses on using an Object model with InterSystems IRIS. The projection of the same data into different models is a valuable part of InterSystems IRIS, as well as the ability to run server-side code.
> However, this challenge is likely unfamiliar, as it deviates from InterSystems IRIS being used as a standard database. Don't let this put you off though!
>For an introduction to using different data models, see the Mutli-model tutorial

Here we are using `irispy`, which is an IRIS native connection in Python. This gives us access to internal classes, methods and proceedures. Using native connections can expose server-side processes to external users. As a result, its possible to run functions directly on the data without having to copy or duplicate the data, all from an external application, which can also retrieve the result. Plus, this can all be done in InterSystems IRIS's secure, user-controlled environment. We are using this to instantiate each product as an object:

```python
item = irispy.classMethodObject("coffeeco.Inventory", "%OpenId", id)
```

So, here we are using the `irispy` method `.classMethodObject()`. This runs a *class method* of a particular class, which is expected to return an *Object* (hence the "Object" at the end). We pass parameters of the class we are using - which is the Persistent class which makes up the database - `coffeeco.Inventory`, then the class method `%OpenId`,  and the class method parameter - the product ID.

This is equivalent to running the ObjectScript command.

```
set item = ##class(coffeeco.Inventoy).%OpenId(id)
```

## Look at product tiles

Now, on the application tab, we can navigate to the "Shop" page. You should see a series of basic'tiles, these have been created by adding one tile per product. However, at the moment, only the selector for quantity and adding to basket are added correctly. Lets add the rest of the product properties to the tiles.

## Adding product properties

Return to the code editor tab and the `pages/products.py` file.  

In the step above, we have instantiated each product in the database as an Object called `item` and passed this into the `write_product_tile`, combined with the product ID and an additional iterator `i` which is used for layout positioning.

Scroll to the `write_product_tile()` function definition. This function adds a container to a column as well as various formatting controls.

For each product, we want to add the Name, Country Of Origin, Description and Price. When using an Object Model, the columns in our relational tables become properties. When using a class object in Python, we can access the database properties with:

```python
item.get("Property Name")
```

So, to complete the tile for each product we need to access each of the properties with `.get()` methods. We will use different streamlit functions to create different header levels: 


Copy the following into line 26 
```python
            ## Write the product name as a header
            st.header(item.get("Name"))

            ## Write other product properties
            st.subheader(f"Origin: {item.get("CountryOfOrigin")}")
            st.write(item.get("Description"))
            st.subheader(f"$ {item.get("Price")}")
```


## Next Steps

Now we have created a complete product page. We are going to largely skip discussion of the adding to basket logic but feel free to explore the code further here or visit the [Project Repository](https://github.com/gabriel-ing/python_coffeeco) to freely access the code. 

The main thing to note is that products added to the basket are saved in the streamlit `st.session_state` object - this is a way of saving data to a session, meaning it persists across different pages. We have create a dictionary accessible at `st.session_state.basket` which has the product ID and quantity in the basket.

For now though. Lets move onto the final step - the checkout!