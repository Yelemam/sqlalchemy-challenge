# sqlalchemy-challenge
![Surf](https://github.com/user-attachments/assets/1f30d0b2-dbfd-40c1-a90b-6bf14e09b028)

# Introduction

You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. 
To help with your trip planning, you decide to do a climate analysis about 
the area. 

# Analysing and Exploring the Climate Data

Python and SQLAlchemy were used to do a basic climate analysis and data exploration 
of the climate database. SQLAlchemy ORM queries, Pandas, and Matplotlib were 
used for the analysis. The complete climate analysis, and data exploration 
was done using python pandas notebook. The Climate starter fileand the
SQLAlchemy (Hawaii.sqlite) were provided. 
 
 1. SQLAlchemy create_engine() function to connect to the SQLite database.
 2. SQLAlchemy automap_base() function to reflect the tables into classes, 
    and then save references to the classes named station and measurement.
 3. Link Python to the database by creating a SQLAlchemy session.

# Precipitation Analysis

   1. Find the most recent date in the dataset.
   2. Using that date, get the previous 12 months of precipitation data by 
      querying the previous 12 months of data.
   3. Load the query results into a Pandas DataFrame. Explicitly set the 
      column names.
   4. Sort the DataFrame values by "date".
   5. Plot the results by using the DataFrame plot method.
      ![Precipitation_Plot](https://github.com/user-attachments/assets/22a54157-410a-490f-af76-b8f77bf58fba)

   7. Use Pandas to print the summary statistics for the precipitation data.
      
# Station Analysis

   1. Design a query to calculate the total number of stations in the dataset.
   2. Design a query to find the most-active stations (that is, the stations
      that have the most rows). To do so, complete the following steps:
      o List the stations and observation counts in descending order.
      o which station id has the greatest number of observations?
   3. Design a query that calculates the lowest, highest, and average 
      temperatures that filters on the most-active station id found in the 
      previous query.
   4. Design a query to get the previous 12 months of temperature 
      observation (TOBS) data. To do so, complete the following steps:
      o Filter by the station that has the greatest number of observations.
      o Query the previous 12 months of TOBS data for that station.
      o Plot the results as a histogram with bins=12
      ![Temp_observed_USC00519281](https://github.com/user-attachments/assets/a26f6cd7-3500-4972-87f4-365398136f3e)

# Part 2: Design Your Climate App
![Climate_app](https://github.com/user-attachments/assets/b6939ad0-f76b-41cb-a97a-2d633e2cd0a9)

# Instructions 

Design a Flask API based on the queries that was just developed. 
To do so, use Flask to create routes as follows:

    1.    / (Homepage)
       o    Start at the homepage.
       o    List all the available routes.
       
    2.    /api/v1.0/precipitation
       o    Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
       o    Return the JSON representation of your dictionary.
       
    3.    /api/v1.0/stations
       o    Return a JSON list of stations from the dataset.
       
    4.    /api/v1.0/tobs
       o    Query the dates and temperature observations of the most-active station for the previous year of data.
       o    Return a JSON list of temperature observations for the previous year.
       
    5.    /api/v1.0/<start> and /api/v1.0/<start>/<end>
       o    Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
       o    For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
       o    For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

# Table of Contents 
   1. Temp_observed_USC00519281.png : Temperature observed at station USC00519281 for the last 12 month 
   2. Precipitation_plot.Png: Precipitation in Honolulu 
   3. climate _starter.ipynb: jubyternotebook file for the climate analysis and exploration 
   4. app.py: Weather app file 
   5. Resources folder containning the two CSV files and sqlite file what were used for our analysis and exploration.
   
