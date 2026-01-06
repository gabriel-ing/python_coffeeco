# Checkout

In the previous step we created a page to add products to the users basket. The final thing to do is to create a checkout page.

Lets take a look at what we have at the moment. Open the app tab and start by navigating to the **Shop** page. Add a couple of items to the basket, then go to checkout with the button at the top of the page, or the link in the left-hand side panel. 

You'll see a summary of the order you've created, with an itemised list of items, as well as a generated total. Great! Lets try to Pay - hit "Pay Now!"

Ah, that button doesn't seem to be working. Lets switch to the code editor and see whats going on with it. 

## Creating the database

The checkout page is created in `app/pages/checkout.py`. Open the code-editor tab and navigate to `pages/checkout.py`.

Again, we won't run through all the logic in the checkout, and instead focus only on how our webpage interacts with our InterSystems IRIS database. Also, for simplicity we're going to skip actually taking the payments — this is a dummy app after all!

Scroll to line 55 - this is where we define the `Pay Now!` button.

You'll see the foloowing 

```python, nocopy
    if st.button("Pay Now!"):
        for id in st.session_state.basket:
            pass
            # Call the function to update the database
            # update_database(id)

```

Right - we must have forgotten to implement the rest of the button's functionality. Lets sort this now. 

So far, when we pay we iterate over the products in the basket by ID. We want to update the database for each product being sold. Lets use an IRIS native connection and the Object model for this. We've actually already created the connection above:

First of all, lets delete the `pass` command, and uncomment the `update_database(id)` line.

```python, nocopy
    connection = iris.connect("localhost", 1972, "USER", "SuperUser", "SYS")
    irispy = iris.createIRIS(connection)
```

So to proceed, we need to:

- Open an object by ID
- Check if the quantity in the basket is equal to the number in stock
    - If True, send an internal alert and delete the item from the inventory
    - If False, set the new stock level to be current stock minus the number in the basket.
        - If the new stock is less than 3, send a low stock warning internally.

So, to start with, lets open the product as an object using `irispy.classMethodObject()`. Add this line into the `for` loop on line 57.

```python
    item = irispy.classMethodObject("coffeeco.Inventory", "%OpenId", id)
```

Now we have our item, we need to check if the basket quantity equals the stock quantity, again add this to the for loop.

```python
if st.session_state.basket[id]["Quantity"] == item.get("StockQuantity"):
        # Send internal alert from the server using pre-written method
        status = irispy.classMethodString("coffeeco.Alerts", "OutOfStockAlert", id, item.get("Name"))
                
        # Delete the item from the database
        irispy.classMethodVoid("coffeeco.Inventory", "%DeleteId", id)
```

Here we use the `irispy` connection to send a pre-configured alert from the server, using the class method `coffeeco.Alerts.OutOfStockAlert`. We won't look further into this, but it demonstrates how we can use internal methods from this external connection.

Now lets write the logic to update the database in the `else` block.

```python
        # Calculate the new quantity in stock
        new_quantity = item.get("StockQuantity") - st.session_state.basket[id]["Quantity"]
                
        # Send alert if stock is low
        if new_quantity<3:
            status = irispy.classMethodString("coffeeco.alerts", "LowStockAlert", id, item.get("Name"))
                
        # Update the quantity in stock
        item.set("StockQuantity", new_quantity) 
                
        # Save the item
        item.invokeVoid("%Save")
```

Here we use the object method for setting a property, `item.set(<property>, <value>)`. We then use `.invokeVoid()` to invoke an object method - in this case the `%Save` method. This saves the changes to the product to the database.

Finally, we will reset the basket and redirect the user. Add these lines to the outside of the for loop:

```python
        st.session_state.basket = {}
        st.switch_page( "pages/hidden/thanks.py")
```

## Next steps

And there we have it – we've completed the checkout! (*we don't actually want to take user's money here...)

In this step, we have seen how the object data model can be used to manage individual entries to the database, how we can use class methods and instantiated object methods, and how we can call server-side functions to send an alert from an external connection.