#!/usr/bin/env python3

from flask import Flask, request, Response
import jsonpickle
import logging

app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)

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
    # retrieves Trip record from trip_overview DB
    # returns JSON response containing trip_id, trip_name, start_date, end_date
    app.logger.info(f"Retrieving trip overview information for trip '{tripName}'...")

    # UPDATE
    response = {'TRIp id' : 100}
    response_pickled = jsonpickle.encode(response)
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