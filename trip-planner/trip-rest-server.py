#!/usr/bin/env python3

from flask import Flask, request, Response
import jsonpickle
import logging
from google.cloud.sql.connector import Connector
import pg8000
import sqlalchemy
from sqlalchemy import text

app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)

# initialize Connector object
connector = Connector()

# function to return the database connection
def getconn():
    conn = connector.connect(
        "trip-planner-442220:us-central1:trip-planner-db",
        "pg8000",
        user="postgres",
        password="TripPl4nn3r!",
        db="postgres"
    )
    return conn

# create connection pool
pool = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

# Test the connection
with pool.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print(result.fetchone())

@app.route('/apiv1/trip', methods=['POST'])
def createTrip():
    # creates new Trip record in trip_overview DB
    # request body should be JSON including trip_name, start_date, end_date
    # returns JSON response containing trip_id, trip_name, start_date, end_date

    app.logger.info(f"Creating new trip...")

    # UPDATE
    response = {'new trip' : 'TRIP'}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/apiv1/trip/<int:tripId>/<dateString>', methods=['PATCH'])
def updateTrip(tripId, dateString):
    # updates field(s) for an existing trip day from trip_details DB
    # identifies record in DB by URL parameters: tripId, dateString
    # need to handle converting dateString into the appropiate type

    app.logger.info(f"Updating trip {tripId} for day {dateString}...")

    # UPDATE
    response = {'tripID' : id}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/apiv1/trip/<tripName>', methods=['GET'])
def getTrip(tripName):
    # retrieves Trip record from trip_overview DB by tripName (trip name unique in database)
    # returns JSON response containing trip_id, trip_name, start_date, end_date
    app.logger.info(f"Retrieving trip overview information for trip '{tripName}'...")

    query = sqlalchemy.text('SELECT * FROM "trip_overview" WHERE trip_name = :tripname')

    with pool.connect() as db_conn:
        # retrieve trip overview 
        trip_overview_data = db_conn.execute(query, {"tripname":tripName}).fetchall()

        # if no tripName is found
        if not trip_overview_data:
            error_resp = {'error': 'Trip not found', 'message': 'No trip data found for the given trip name.'}
            return Response(response=jsonpickle.encode(error_resp), status=404, mimetype="application/json")

        trip = trip_overview_data[0]
        
        # formulate json response
        json_resp = {'trip_id' : trip[0], 'trip_name' : str(trip[1]), 'start_date' : str(trip[2]), 'end_date' : str(trip[3]) }

        db_conn.commit()


    response_pickled = jsonpickle.encode(json_resp)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/apiv1/tripDays/<int:tripId>', methods=['GET'])
def getTripDayDetails(tripId):
    # retrieves all Trip Day records from trip_details DB with matching tripId
    # request body should include tripId
    # returns JSON response containing list of records, each record includes:
    # {trip_id, date, location, accomodation, travel, activities, dining, notes}

    app.logger.info(f"Retrieving trip day information for trip {tripId}...")

    # UPDATE
    response = {'TRIp id' : 100}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/apiv1/addDocument/<int:tripId>', methods=['POST'])
def addDocument(tripId):
    app.logger.info(f"Adding trip document associated with trip {tripId} to object store...")
    # user id in request body, associate this user with group

    # UPDATE
    response = {'Doc added' : 'auccessfully'}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
app.run(host="0.0.0.0", port=4000)