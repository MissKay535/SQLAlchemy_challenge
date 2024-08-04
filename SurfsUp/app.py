# Import dependencies and setup
import numpy as np
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func


# Import Flask
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# # View all of the classes that automap found
# Base.classes.keys()

# # Save references to each table
# Measurement = Base.classes.measurement
# Station = Base.classes.station


#################################################
# Flask Setup
#################################################


#################################################
# Flask Routes
#################################################
