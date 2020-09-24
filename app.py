# Importing dependencies
from flask import Flask, jsonify
import datetime as dt
import numpy as np
import pandas as pd

# Importing SQLAlcchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Database setup
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session link from Python to database
session = Session(engine)

# Create new FLask app instance
app = Flask(__name__)

# Creating routes
# Define app starting point or 'root'
@app.route('/' )
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!\n
    Available Routes:\n
    /api/v1.0/precipitation\n
    /api/v1.0/stations\n
    /api/v1.0/tobs\n
    /api/v1.0/temp/start/end\n
    ''')

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate date one year ago from most recent date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query to get date and precipitation for previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    # Create a dictionary with date as the key and the preciptation as the value
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Stations route
@app.route("/api/v1.0/stations")
def stations():
    # Query to get all of the staions in database
    results = session.query(Station.station).all()
    # Unravel results into one-demensional array and conver to a list
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Monthly Tempurature route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    # Calculate date one year ago from most recent date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        # Query primary station for all the temperature observations from previous year
    results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all()
    # Unravel results into one-demensional array and conver to a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Statistics route
# Add starting and end date routes
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    # Query to select minimum, average, and maximum temperatures from SQLite database
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    # Determine starting and ending date
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
        # Query database with 'sel' list
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    # Unravel results into one-dememsional array and covert to list
    temps = list(np.ravel(results))

    return jsonify(temps=temps)
