# Streamlit App

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


### Stock Management. 

We haven't built the products page yet, so lets not see whats there quite yet. First, lets make sure the stock is up to date. 

Open the `Stock Management` page from the sidebar. You'll be prompted for log-in details. Luckily no-one has changed these from the default yet, so the log in is currently:
    
- Username: admin
- Password: 1234

If you were to take a look at the stock_management.py page, you'd see these hard-coded in at the moment. It barely needs stating that this is terrible practice, never hard-code the password in production. 

