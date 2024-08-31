import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes for Hawaii Weather Data:<br/><br>"
        f"-- Daily Precipitation Totals for Last Year: <a href=\"/api/v1.0/precipitation\">/api/v1.0/precipitation<a><br/>"
        f"-- Active Weather Stations: <a href=\"/api/v1.0/stations\">/api/v1.0/stations<a><br/>"
        f"-- Daily Temperature Observations for Station USC00519281 for Last Year: <a href=\"/api/v1.0/tobs\">/api/v1.0/tobs<a><br/>"
        f"-- Min, Average & Max Temperatures for Date Range: <a href=\"/api/v1.0/trip/yyyy-mm-dd/yyyy-mm-dd\">/api/v1.0/trip/yyyy-mm-dd/yyyy-mm-dd</a><br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Creating  session from Python to the DB
    session = Session(engine)

    """Return a list of all daily precipitation totals for the last year"""
    # Query and summarize daily precipitation across all stations for the last year of available data
    
    start_date = '2016-08-23'
    sel = [measurement.date,
        func.sum(measurement.prcp)]
    precipitation = session.query(*sel).\
            filter(measurement.date >= start_date).\
            group_by(measurement.date).\
            order_by(measurement.date).all()
   
    session.close()

    # Return a dictionary with the date as key and the daily precipitation total as value
    precp_dates = []
    precp_total = []

    for date, dailytotal in precipitation:
        precp_dates.append(date)
        precp_total.append(dailytotal)
    
    precp_dict = dict(zip(precp_dates, precp_total))

    return jsonify(precp_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Creating session from Python to the DB
    session = Session(engine)

    """Return a list of all the active Weather stations in Hawaii"""
    # Return a list of active weather stations in Hawaii
    sel = [measurement.station]
    active_stations = session.query(*sel).\
        group_by(measurement.station).all()
    session.close()

   
    # Convert list into normal list and return the JSonified list
    
    list_of_stations = list(np.ravel(active_stations))
    return jsonify(list_of_stations)

   
@app.route("/api/v1.0/tobs")
def tobs():
    # Creating session from Python to the DB
    session = Session(engine)
    # Query the last 12 months of temperature observation data for the most active station
    start_date = '2016-08-23'
    most_active_station = 'USC00519281'
    sel = [measurement.date,
        measurement.tobs]
    station_temps = session.query(*sel).\
            filter(measurement.date >= start_date, measurement.station == most_active_station).\
            group_by(measurement.date).\
            order_by(measurement.date).all()

    session.close()

    # Return a dictionary with the date as key and the daily temperature observation as value
    obs_dates = []
    temp_obs = []

    for date, obs in station_temps:
        obs_dates.append(date)
        temp_obs.append(obs)
    
    most_active_tobs_dict = dict(zip(obs_dates, temp_obs))

    return jsonify(most_active_tobs_dict)


@app.route("/api/v1.0/trip/<start_date>")
def trip1(start_date):
    # Calculate minimum, average, and maximum temperatures from the start date onward.
    session = Session(engine)
    query_result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).all()
    session.close()

    # Prepare the response
    if query_result and query_result[0][0] is not None:  # Check if the result is not empty and not None
        min_temp, avg_temp, max_temp = query_result[0]
        trip_stats = {
            "Min": min_temp,
            "Average": avg_temp,
            "Max": max_temp
        }
        return jsonify(trip_stats)
    else:
        return jsonify({"error": f"Date {start_date} not found or not formatted as YYYY-MM-DD."}), 404

@app.route("/api/v1.0/trip/<start_date>/<end_date>")
def trip2(start_date, end_date):

    # Calculate minimum, average, and maximum temperatures for the specified date range.
    session = Session(engine)
    query_result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    session.close()

    # Prepare the response
    if query_result and query_result[0][0] is not None:  # Check if the result is not empty and not None
        min_temp, avg_temp, max_temp = query_result[0]
        trip_stats = {
            "Min": min_temp,
            "Average": avg_temp,
            "Max": max_temp
        }
        return jsonify(trip_stats)
    else:
        return jsonify({"error": f"Date(s) not found, invalid date range, or dates not formatted correctly."}), 404

if __name__ == '__main__':
    app.run(debug=True)
