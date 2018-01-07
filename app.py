# design a flask api
from flask import Flask
from flask import jsonify

# Python SQL toolkit and Object Relational Mapper
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, extract
import numpy as np

# Create Database Connection
engine = create_engine('sqlite:///hawaii2.sqlite')

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine,reflect=True)

# create a reference of the classes
S=Base.classes.station
# create a reference of the classes
M=Base.classes.measurement

# Using the references to classes, start querying the database
from sqlalchemy.orm import Session
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

#Session management with scoped session (Session that is universal across all threads in the code)
session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)



# Querying the database 
prcp_data = session.query(M.date,M.prcp).filter(M.date >= '2016-08-01').filter(M.date <='2017-08-01').all()
# Unpacking the tuple into separate lists
dates_p=[res[0] for res in prcp_data]
prcp_p = [res[1] for res in prcp_data]
# combining the above lists into dictionary
prcp_dict = dict(zip(dates_p,prcp_p))

# querying the db
stations = session.query(S.station)
# unpacking the tuple into separate lists
station = [res[0] for res in stations]

temp_obs = session.query(M.tobs).filter(M.date >= '2016-12-31').filter(M.date <='2017-12-31').all()
temp = [res[0] for res in temp_obs]


# Create an app, being sure to pass __name__
app = Flask(__name__)

# Define what to do when a user hits the index route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/preciptation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/enter start date <br/>"
        f"/api/v1.0/enter start date/enter end date <br/>"
    )

@app.route("/api/v1.0/preciptation")
def preciptation():
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    return jsonify(station)


@app.route("/api/v1.0/tobs")
def tobs():
    return jsonify(temp)


@app.route("/api/v1.0/<start_date>")
def temps(start_date):
    return jsonify(session.query(func.min(M.tobs), func.avg(M.tobs), func.max(M.tobs)).\
        filter(M.date >= start_date).all())


@app.route("/api/v1.0/<start_date>/<end_date>")
def temp_end(start_date,end_date):
    return jsonify(session.query(func.min(M.tobs), func.avg(M.tobs), func.max(M.tobs)).\
        filter(M.date >= start_date).filter(M.date<= end_date).all())

if __name__ == "__main__":
    app.run(debug=True)
