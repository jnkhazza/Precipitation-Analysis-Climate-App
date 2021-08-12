import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

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
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to the Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/start/YYYY-MM-DD <br/>"
        f"/api/v1.0/range/YYYY-MM-DD/YYYY-MM-DD <br/>"
        "<br/>"
        f"Please enter date(s) between 2010/01/01 and 2017/08/23"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    
    results = session.query(measurement.date, measurement.prcp).\
                   filter(measurement.date >= query_date).all()
    session.close()
    
    precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict[date] = prcp
        precip.append(precip_dict)

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")
    session = Session(engine)
    
    rows = session.query(measurement)
    
    session.close()
    
    stations = []
    for row in rows:
        stations.append(row.station)
    station_list = set(stations)
    
    test = []
    for i in station_list:
        test.append(i)
    
    return jsonify(test)

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Temp' page...")
    session = Session(engine)
    
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    
    temp_data = session.query(measurement.date,measurement.tobs).\
            filter(measurement.date >= query_date).\
            filter(measurement.station == "USC00519281").\
            order_by(measurement.tobs.desc()).all()
    
    session.close()
    
    temp = []
    for date, prcp in temp_data:
        temp_dict = {}
        temp_dict[date] = prcp
        temp.append(temp_dict)

    return jsonify(temp)

@app.route("/api/v1.0/start/<start>")
def date(start):
    print("Server received request for 'Start' page...")
    session = Session(engine)
   
    sel = [func.min(measurement.tobs),
          func.max(measurement.tobs),
          func.avg(measurement.tobs)]
    
    start_data = session.query(*sel).\
            filter(measurement.date >= start)

    session.close()
        
    start_x = []
    for min, max, avg in start_data:
        start_dict = {}
        start_dict["Min"] = min
        start_dict["Max"] = max
        start_dict["Avg"] = avg
        start_x.append(start_dict)

    return jsonify(start_x)
    

@app.route("/api/v1.0/range/<start>/<end>")
def date_range(start, end):
    """Return TMIN, TAVG, TMAX."""
    session = Session(engine)
  
    sel = [func.min(measurement.tobs),
          func.max(measurement.tobs),
          func.avg(measurement.tobs)]
    
    range_data = session.query(*sel).\
            filter(measurement.date >= start).\
            filter(measurement.date <= end).all()
    
    session.close()
    
    range_x = list(np.ravel(range_data))

    return jsonify(range_x)
    

if __name__ == "__main__":
    app.run(debug=True)

