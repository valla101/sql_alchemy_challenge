from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from datetime import datetime

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect = True)

Base.classes.keys()

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

app = Flask(__name__)
@app.route("/")
def home():
    return ("<br>List of all directories:</br>"
    "<br>/api/v1.0/precipitation</br>"
    "<br>/api/v1.0/stations</br>"
    "<br>/api/v1.0/tobs</br>")

@app.route("/api/v1.0/precipitation")
def class2():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Measurement.id, Measurement.station, Measurement.date, Measurement.prcp).\
            filter(Measurement.date > dt.date(2016, 8, 22)).all()
    session.close()

    all_rows = []
    for id, station, date, prcp in results:
        precip_dict = {}
        precip_dict["id"] = id
        precip_dict["station"] = station
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_rows.append(precip_dict)

    return jsonify(all_rows)

@app.route("/api/v1.0/stations")
def class3():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    stations_unique = session.query(Station.station, Station.name).group_by(Station.station).all()
    session.close()

    all_rows = []
    for station, name in stations_unique:
        stations_dict = {}
        stations_dict["station"] = station
        stations_dict["name"] = name
        all_rows.append(stations_dict)

    return jsonify(all_rows)

@app.route("/api/v1.0/tobs")
def class4():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    most_active_station = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date > dt.date(2016, 8, 22)).all()
    session.close()

    all_rows = []
    for tobs in most_active_station:
        stations_dict = {}
        stations_dict["tobs"] = tobs
        
        all_rows.append(stations_dict)

    return jsonify(all_rows)



@app.route("/api/v1.0/<start>")
def class5(start):
    date_format = '%Y-%m-%d'
    try:
        datetime.strptime(str(start), date_format)
    except ValueError:
        return 'Incorrect date format, should be YYYY-MM-DD'
    session = Session(engine)
    input_date = session.query(func.min(Measurement.tobs).label("Minimum_Tempreature"),
                func.avg(Measurement.tobs).label("Average_Tempreature"),
                func.max(Measurement.tobs).label("Maximum_Tempreature")).\
        filter(Measurement.date >= start).all()
    session.close()

    return jsonify(input_date)

@app.route("/api/v1.0/<start>/<end>")
def class6(start, end):
    date_format = '%Y-%m-%d'
    try:
        datetime.strptime(str(start), date_format)
        datetime.strptime(str(end), date_format)
    except ValueError:
        return 'Incorrect date format, should be YYYY-MM-DD'
    session = Session(engine)
    input_dates = session.query(func.min(Measurement.tobs).label("Minimum_Tempreature"),
                func.avg(Measurement.tobs).label("Average_Tempreature"),
                func.max(Measurement.tobs).label("Maximum_Tempreature")).\
        filter(Measurement.date >= start, Measurement.date < end).all()
    session.close()

    return jsonify(input_dates)
# Start & End date query
# Should probably have a variable that will read the input and convert it into a date. Same for End Date query
# Must create a function to take the date interval and scan for highest temp and lowest temp within that range (func.max(Measurement.tobs))
# Create an empty list and append the scanned objects into empty list

if __name__=="__main__":
    app.run(debug=True)