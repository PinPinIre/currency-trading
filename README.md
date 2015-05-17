## Currency Trading App

This is a small web app written in Flask for posting currency trading requests. The trading views are rate limited based on a users id number and requests are made by posting JSON to the /trade views

### Technologies
I would advise using a Sqlite or Postgres for the database. This is used for user accounts and for trade requests.

A Redis database is used for the rate limiting component of the application.

To run the application you must set environment variables for 'CF_SECRET_KEY' (The secret key for the application), 'DATABASE_URL' (The url to your sql database) and REDIS_URL (The url to your Redis database).

#### TODO
* KISS
* ~~Add user and trade models~~
* ~~Add form validation for login and registration~~
* ~~Use bcrypt or PBKDF2 for passwords~~
* ~~Add rate limit decorator to view (Use Redis?)~~
*   ~~Limit on IP and login~~
*   ~~Coarse and fine-grained limiting~~
* ~~Add a css theme to the app~~
* ~~Add a basic list of trades~~
* ~~Store trade requests to sql db (Mongo as alt?)~~
* ~~Add JS to POST trade requests~~
* ~~Handle success and failure requests~~
* Unit tests
* Process data for D3 Graphs
