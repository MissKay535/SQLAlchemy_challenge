# SQLAlchemy_challenge
Using Python, SQLAlchemy ORM queries, Pandas, and Matplotlib to analyze and do data exploration of a climate database

Instructions:

    Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area. The following sections outline the steps that you need to take to accomplish this task.

Part 1: Analyze and Explore the Climate Data

In this section, you’ll use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, you’ll use SQLAlchemy ORM queries, Pandas, and Matplotlib. To do so, complete the following steps:

    Use the SQLAlchemy create_engine() function to connect to your SQLite database.

    Use the SQLAlchemy automap_base() function to reflect your tables into classes, and then save references to the classes named station and measurement.

    Link Python to the database by creating a SQLAlchemy session.

    Perform a precipitation analysis and then a station analysis by completing the steps in the following two subsections.

Precipitation Analysis

    Find the most recent date in the dataset.

    Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.

    Load the query results into a Pandas DataFrame. Explicitly set the column names.

    Sort the DataFrame values by "date".

    Plot the results by using the DataFrame plot method, as the following image shows:

        A screenshot depicts the plot.

        Use Pandas to print the summary statistics for the precipitation data.

Station Analysis

    Design a query to calculate the total number of stations in the dataset.

    Design a query to find the most-active stations (that is, the stations that have the most rows).

    Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.

    Design a query to get the previous 12 months of temperature observation (TOBS) data. To do so, complete the following steps:

        Filter by the station that has the greatest number of observations.

        Query the previous 12 months of TOBS data for that station.

        Plot the results as a histogram with bins=12

        Close your session.

Part 2: Design Your Climate App

Now that you’ve completed your initial analysis, you’ll design a Flask API based on the queries that you just developed. 