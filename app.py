import datetime as dt
import numpy as np
import pandas as pd
import datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii2.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
M = Base.classes.measurement
S = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


####
#precipitation
####
prcp=session.query(M.date, M.prcp).filter(M.date > '2016-08-23' ).order_by(M.date).all()


####
#Station
####
allstations=session.query(M.station, func.count(M.station)).group_by(M.station).all()

####
#tobs
####
tobs_lastyear=session.query(M.tobs).filter((M.date > '2016-12-31')& (M.date < '2017-12-31')).order_by(M.date).all()

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
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of precipitation data"""
    return jsonify(prcp)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations data"""
    return jsonify(allstations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of tobs data"""
    return jsonify(tobs_lastyear)

@app.route('/api/v1.0/<start>')
def start_date(start):
   return 'Start Date %s' % start

if __name__ == '__main__':
    app.run(debug=True)