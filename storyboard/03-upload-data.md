# Uploading data

In the previous step, we implemented a method to retrieve data from the database using SQLAlchemy, allowing our shop administrator to view the current stock levels in the inventory table.

In this step, we are going to create a method to upload new products into the database. When ordering products from our suppliers, they provide an order-manifest that includes all the information we need in our table. Conviently their table names match ours (...let's not dwell on this coincidence for now), so we just need to upload each datapoint, or update any existing products to our data table. 

This process is also going to take place in the Manage Stock page, so again we are using the stock_management.py file

## File Uploader widget

The first step is to create a file uploader widget which can take a csv file. Then, upon upload we want to create an editable preview of the file, and a button to add the dataframe to the database.

As we are running on a sandbox environment, uploading a file isn't ideal, so instead we are going to paste in the csv file into a text box. However, logic for using a file upload is shown in the stock_management.py file (commented out) for reference. To create the text box upload, paste the following code block to the end of the file: 

```python
    # Create text box to paste in csv data
    csv_text = st.text_area("Paste CSV here", key=f"uploader_{st.session_state.uploader_key}")

    if csv_text:
        
        df = pd.read_csv(io.StringIO(csv_text))

        # Display data in an editable format.
        df = st.data_editor(df)

        # Create a button to add the stock to the database
        if st.button("Add To Database"):
            # Calls the add_to_database function with the dataframe
            add_to_database(df)

            # Reset the file uploader once an order is uploaded to the database
            st.session_state.uploader_key += 1
            df = None

            # Refresh the page to see changes
            st.rerun() 
    
```

## Uploading data to the database

Now we need to define the `add_to_database()` function. This function needs to:

    - Check if the dataframe matches the require schema
    - Get a list of ProductId values currently in the database
    - Split the new dataframe into existing products and new products
    - Add the stock to the existing product rows in the coffeeco.Inventory table
    - Add the new products to the coffeeco.Inventory table

If you scroll to line 37, you'll see that much of this has already been written successfully. In fact, the only thing missing is the conversion of the dataframe to a list of lists with each one being a row, and the execution of the query. 

Try writing these two lines yourself, feel free to copy the set up for the updating part above (exisiting_products_df), although remember this time you need all the columns!

If you need help, the solution will be at the bottom of the page. 

## Testing our upload

We've now implemented the functionality of uploading an order manifest csv file (or pasting it in) and then uploading it to the database using `INSERT` and `UPDATE` queries. Lets see if this works. 

Navigate to the app tab, and refresh the app page (don't refresh your browser! Theres a separate icon within the sandbox window). 

You'll need to re-enter the credentials (admin | 1234) as changing the code refreshes the session.

Into the text box, paste the following csv file: 

```csv
ProductId,Name,Description,CountryOfOrigin,Price,StockQuantity
1003, Arabica Gold,Smooth and aromatic with a hint of chocolate,Colombia,15.99,5
1006, Robusta Strong,Bold and intense flavor with high caffeine,Vietnam,12.49,3
1007, Ethiopian Sunrise,Fruity and floral notes with a bright finish,Ethiopia,18.75,7
1103, Sumatra Dark,Earthy and full-bodied with low acidity,Indonesia,16.5,2
1021, Brazilian Classic,Nutty and sweet with a smooth texture,,14.2,1
1001, Colombian Supremo, Smooth and balanced with notes of chocolate and caramel., Columbia, 12.5, 3
```

Oh no! Theres a value missing - the supplier has missed the CountryOfOrigin for the Brazillian Classic. Luckily we made this table editable, so double click the empty box and add in a suitable value. Feel free to change some other values here if you'd like as well

When you've done this, click "Add to Database". You'll see the page refresh and hopefully the changes will appear in the stock table displayed.