#!/usr/bin/env python
# coding: utf-8

# # Flask Task

# In[ ]:


import numpy as np
import datetime as dt
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


# Setup d/b

engine = create_engine("sqlite:///hawaii.sqlite",connect_args={'check_same_thread': False})
Base = automap_base()
conn = engine.connect()
#reflect tables
Base.prepare(engine, reflect=True)


# Save reference to the table

Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)
                                                               

#Create app & first route

app = Flask(__name__)


@app.route("/")

def home():
    return (f"Welcome to the Hawaii Holiday Weather API<br/>"
    f"Available Routes:<br/>"
    f"A list of a year's worth of precipitation readings from all stations reporting in Hawaii: /api/v1.0/hawaii_holiday/precipitation<br/>"
    f"A list of all stations reporting in Hawaii:  /api/v1.0/hawaii_holiday/station<br/>"
    f"A list of a year's worth of temperatures from all stations reporting in Hawaii:  /api/v1.0/hawaii_holiday/tobs<br/>"
    f"Enter a start date (format:  YYYY-MM-DD) to calculate the Min, AVG and Max temperature for that date to the most recent date recorded:  /api/v1.0/hawaii_holiday/start<br/>"
    f"Enter a start and end date (format: YYYY-MM-DD) to calculate the Min, AVG and Max temperature for the selected time frame:   /api/v1.0/hawaii_holiday/startend<br/>"
           )

#Second Route

@app.route("/api/v1.0/hawaii_holiday/precipitation")

def precipitation():
    recent_prcp = session.query(str(Measurement.date), Measurement.prcp)\
    .filter(Measurement.date > '2016-08-22')\
    .filter(Measurement.date <= '2017-08-23').all()

    # convert results to a dictionary with date as key and prcp as value
    prcp_dict = dict(recent_prcp)

    # return json list of dictionary
    return jsonify(prcp_dict)


# Third route

            
@app.route("/api/v1.0/hawaii_holiday/stations")
        
            
def stations():
 
    stations_query = session.query(Station.name, Station.station).all()
    station_d = dict(stations_query)
    
    return jsonify(station_d)

#Fourth Route

@app.route("/api/v1.0/hawaii_holiday/tobs")

def tobs():
  
    tobs = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.station == 'USC00519281')\
    .filter(Measurement.date > '2016-08-23')\
    .filter(Measurement.date <= '2017-08-23')\
    .all()
            
    #list of dicts for date and tobs as keys and values
    temperatures = []
    for result in temperatures:
            row = {}
            row["date"] = tobs[0]
            row['tobs'] = tobs[1]
            temperatures.append(row)
            
    return jsonify(temperatures)


#API Dynamic Routes: Start 

#start route: accepts start date as a parameter from the url & 
            #returns the min, max, ave temps calced from given start date to end of the dataset

@app.route("/api/v1.0/hawaii_holiday/<start>")
def here(start):
            
    start_date = dt.datetime.strptime(start, "%d %m, %Y")
    end_date = dt.date('2017-08-23')
    data_query = (func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    data = list(np.ravel(data_query))
    
    return jsonify(data)


# Dynamic Routes: start.end 

@app.route("/api/v1.0/hawaii_holiday/<start>/<end>")
def herethere(start,end):
            
    start_date = dt.datetime.strptime(start, "%d %m, %Y")
    end_date = dt.datetime.strptime(end, "%d %m, %Y")
    data_query = (func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    data = list(np.ravel(data_query))
    
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=False)
            
# Close Session
session.close()


# In[ ]:





# In[ ]:




