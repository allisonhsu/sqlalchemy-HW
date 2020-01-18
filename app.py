import numpy as np
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
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    prcpdata = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    precipitation = []
    for date, prcp in prcpdata:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    list_station = session.query(Station.station).all()

    session.close()

    return jsonify(list_station)

## start from here later..... (1/11/20)
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    histogram = session.query(Measurement.station,Measurement.date,Measurement.tobs).\
                filter(Measurement.date > '2016-08-23', Measurement.date <= '2017-08-23').\
                order_by(Measurement.date).all()
    
    session.close()
    
    date_temp = []
    for station, date, tobs in histogram:
        tobs_dict ={}
        tobs_dict["Station"]=station
        tobs_dict["Date"]=date
        tobs_dict["tobs"]= tobs
        date_temp.append(tobs_dict)
    
    return jsonify(date_temp)

@app.route("/api/v1.0/<start_date>")
def start(start_date):
    session = Session(engine)

    start_tob = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= '2017-08-23').all()
    
    session.close()
    
    return jsonify(start_tob)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date,end_date):

    session = Session(engine)

    start_end_tob = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    
    session.close()
    
    return jsonify(start_end_tob)



if __name__ == '__main__':
    app.run(debug=True)
