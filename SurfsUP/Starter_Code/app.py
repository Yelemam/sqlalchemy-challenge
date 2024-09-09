# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template_string, request, redirect, url_for

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

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
@app.route("/", methods=['GET', 'POST'])
def welcome():
    """List all available api routes."""
    if request.method == 'POST':
        if 'start_date' in request.form:
            start_date = request.form['start_date']
            return redirect(url_for('stats', start=start_date))
        elif 'range_start_date' in request.form and 'range_end_date' in request.form:
            start_date = request.form['range_start_date']
            end_date = request.form['range_end_date']
            return redirect(url_for('stats', start=start_date, end=end_date))

    return render_template_string("""
    <html>
        <head>
            <title>Climate App API</title>
            <style>
                h1 {
                    text-align: center;
                    background-color: #4CAF50;
                    color: yellow;
                    padding: 20px;
                    margin-top: 0;
                }
                
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: lightblue;
                }
                .container {
                    width: 80%;
                    margin: 0 auto;
                    padding: 20px;
                }
                p {
                    background-color: #4CAF50;
                    color: yellow;
                    margin:  auto;
                    padding: 20px;
                    width: 30%;
                    text-align: center;
                    font-size: 16px;
                }
            </style>
        </head>
        <body>
            <h1>Welcome to the Climate App API!</h1>
            <div class="container">
                <h2>Available Routes:</h2>
                <ul>
                    <li><a href="{{ url_for('precipitation') }}">Daily Precipitation Totals for The Target Year</a></li>
                    <li><a href="{{ url_for('stations') }}">List of Weather Stations</a></li>
                    <li><a href="{{ url_for('tobs') }}">Temperature Observations for The Most Active Station</a></li>
                    <li>
                        Temperature Statistics for a given Date:
                        <form method="POST">
                            <input type="date" name="start_date" required>
                            <input type="submit" value="Get Data">
                        </form>
                    </li>
                    <li>
                        Temperature Statistics for Date Range:
                        <form method="POST">
                            <input type="date" name="range_start_date" required>
                            <input type="date" name="range_end_date" required>
                            <input type="submit" value="Get Data">
                        </form>
                    </li>
                </ul>
            </div>
            <footer>
                <p>Yara El Emam, Copyrights 2024</p>
            </footer>
        </body>
    </html>
    """)


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date 1 year from the last data point in the database
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year_ago = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query for the date and precipitation for the last year
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).\
        order_by(Measurement.date).all()

    session.close()

    # Convert the query results to a dictionary
    precipitation_dict = {date: prcp for date, prcp in results}

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date 1 year ago from the last data point in the database
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year_ago = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Find the most active station
    most_active_station = session.query(Measurement.station, func.count(Measurement.station).label('count')).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()

    # Get the station name
    station_name = session.query(Station.name).\
        filter(Station.station == most_active_station.station).first()

    # Query the primary station for all tobs from the last year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == most_active_station.station).\
        filter(Measurement.date >= one_year_ago).all()

    session.close()

    # Convert list of tuples into normal list
    temps = list(np.ravel(results))

    # Prepare the response
    response = {
        "station_id": most_active_station.station,
        "station_name": station_name[0] if station_name else "Unknown",
        "temperature_observations": temps
    }

    return jsonify(response)
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start, end=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
    else:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()

    session.close()

    # Convert list of tuples into normal list
    temps = list(np.ravel(results))

    return jsonify({"TMIN": temps[0], "TAVG": temps[1], "TMAX": temps[2]})

if __name__ == '__main__':
    app.run(debug=True)
