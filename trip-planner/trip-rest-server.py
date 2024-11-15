#!/usr/bin/env python3

from flask import Flask, request, Response
import jsonpickle
import logging

app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)

@app.route('/apiv1/trip', methods=['POST'])
def createTrip():
    app.logger.info(f"Creating new trip...")

    # UPDATE
    response = {'new trip' : 'TRIP'}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/apiv1/trip/<int:id>', methods=['PATCH'])
def updateTrip(id):
    app.logger.info(f"Updating trip with ID: {id}...")

    # UPDATE
    response = {'tripID' : id}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/apiv1/tripId/<group>', methods=['GET'])
def getTripId(group):
    app.logger.info(f"Retrieving trip ID associated with group {group}...")

    # UPDATE
    response = {'TRIp id' : 100}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/apiv1/addDocument/<int:id>', methods=['POST'])
def addDocument(id):
    app.logger.info(f"Adding trip document associated with trip {id} to object store...")
    # user id in request body, associate this user with group

    # UPDATE
    response = {'Doc added' : 'auccessfully'}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
app.run(host="0.0.0.0", port=4000)