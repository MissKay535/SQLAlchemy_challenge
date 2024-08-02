# Import dependencies and setup
import numpy as np
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Flask
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def homepage():
     """All available API routes."""
     return (
         f"Welcome to SurfsUp API<br/>"
         f"Available Routes:<br/>"
         f"_______________________<br/>"
         f"Precipitation data for last 12 months (24/08/2016 to 23/08/2017):<br/>"
         f"/api/v1.0/precipitation<br/>"
         f"_______________________<br/>"
         f"List of stations:<br/>"
         f"/api/v1.0/stations<br/>"
         f"_______________________<br/>"
         f"Date and temperature observations of the most-active station (USC00519281) for the past 12 months:<br/>"
         f"/api/v1.0/tobs<br/>"
         f"_______________________<br/>"
         f"Minimum, maximum, and average temperature from a given start date to end of dataset:<br/>"
         f"Please enter Start Date in the format: YYYY-MM-DD<br/>"
         f"/api/v1.0/<start><br/>"
         f"_______________________<br/>"
         f"Minimum, maximum, and average temperature from a given start date to a given end date:<br/>"
         f"Please enter Start Date and End Date in the format: YYYY-MM-DD/YYYY-MM-DD<br/>"
         f"/api/v1.0/<start>/<end><br/>"
         f"_______________________"
     )


@app.route("/api/v1.0/precipitation")
def precipitation():
     """Retrieve last 12 months of data"""

     # Create our session (link) from Python to the DB
     session = Session(engine)

     # Convert the query results from your precipitation analysis 
     # (i.e. retrieve only the last 12 months of data) to a dictionary 
     # using date as the key and prcp as the value.

     # Find the most recent date in the dataset.
     recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

     # Calculate the date one year from the last date in data set.
     past_year_data = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

     # Perform a query to retrieve the data and precipitation scores
     prcp_scores = session.query(Measurement.date, Measurement.prcp).\
                     filter(Measurement.date >= past_year_data).\
                     order_by(Measurement.date).all()
    
     # Close the session
     session.close()
    
     # Create a dictionary using date as the key and prcp as the value
     precipitation_dict = {}
     for date, prcp in prcp_scores:
         precipitation_dict[date] = prcp
    
         # Return the JSON representation of dictionary.
     return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def stations():
     """Get a list of stations"""
    
     # Create our session (link) from Python to the DB
     session = Session(engine)

     # Perform a query to retrieve the station data
     station_data = session.query(Station.station).all()
    
     # Close the session
     session.close()
    
     # Convert list of tuples into normal list
     station_list = list(np.ravel(station_data))
    
     # Return a JSON list of stations from the dataset.
     return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
     """Temperature data for the most active station during the past 12 months"""
    
     # Create our session (link) from Python to the DB
     session = Session(engine)

     # Find the most recent date in the dataset.
     recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

     # Calculate the date one year from the last date in data set.
     past_year_data = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

     # Find the most active station id
     most_active_station = session.query(Measurement.station).\
                             group_by(Measurement.station).\
                             order_by(func.count(Measurement.station).desc()).first()
     most_active_station = most_active_station[0]

     # Perform a query to get the dates and temperature observations of the most-active station
     # for the previous year of data
     station_temp_data = session.query(Measurement.date, Measurement.tobs).\
                                 filter(Measurement.station == most_active_station).\
                                 filter(Measurement.date >= past_year_data).\
                                 order_by(Measurement.date).all()
    
     # Close the session
     session.close()
    
     # Create a list of dictionary containing dates and temperatures observations
     station_temp_list = []
     for date, temp in station_temp_data:
         station_temp_dict = {}
         station_temp_dict["date"] = date
         station_temp_dict["temp"] = temp
         station_temp_list.append(station_temp_dict)
    
     # Return a JSON list of temperature data of previous year for the most active station (USC00519281)
     return jsonify(station_temp_list)


@app.route("/api/v1.0/<start>")
def start(start):
     """Min, max, and average temperature data from start date"""
    
     # Create our session (link) from Python to the DB
     session = Session(engine)

     # Create list for date and temperature values
     sel = [Measurement.date,
            func.min(Measurement.tobs), 
            func.max(Measurement.tobs), 
            func.avg(Measurement.tobs)]

     # Perform a query to get TMIN, TAVG, and TMAX for all the dates 
     # greater than or equal to the start date, taken as a parameter from the URL
     start_data = session.query(*sel).\
                     filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).\
                     group_by(Measurement.date).\
                     order_by(Measurement.date).all()
    
     # Close the session
     session.close()

     # Create a list of dictionary to store date, min, max and avg temperature values
     start_data_list = []
     for date, min, max, avg in start_data:
         start_dict = {}
         start_dict["date"] = date
         start_dict["min_temp"] = min
         start_dict["max_temp"] = max
         start_dict["avg_temp"] = avg
         start_data_list.append(start_dict)
    
     # Return a JSON list of the minimum temperature, the average temperature, and the
     # maximum temperature calculated from the given start date to the end of the dataset
     return jsonify(start_data_list)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
     """Min, max, and average temperature data from start date to end date"""
    
     # Create our session (link) from Python to the DB
     session = Session(engine)

     # Create list for date and temperature values
     sel = [Measurement.date,
            func.min(Measurement.tobs), 
            func.max(Measurement.tobs), 
            func.avg(Measurement.tobs)]

     # Perform a query to get TMIN, TAVG, and TMAX for all the dates from start date to
     # end date inclusive, taken as parameters from the URL
     start_end_data = session.query(*sel).\
                     filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).\
                     filter(func.strftime("%Y-%m-%d", Measurement.date) <= end).\
                     group_by(Measurement.date).\
                     order_by(Measurement.date).all()
    
     # Close the session
     session.close()

     # Create a list of dictionary to store date, min, max and avg temperature values
     start_end_data_list = []
     for date, min, max, avg in start_end_data:
         start_dict = {}
         start_dict["date"] = date
         start_dict["min_temp"] = min
         start_dict["max_temp"] = max
         start_dict["avg_temp"] = avg
         start_end_data_list.append(start_dict)
    
     # Return a JSON list of the minimum temperature, the average temperature, and the
     # maximum temperature calculated from the given start date to the given end date
     return jsonify(start_end_data_list)


#################################################

if __name__ == '__main__':
          app.run(debug=True)