#!/usr/bin/env python3

from flask import Flask, request, Response
import jsonpickle
import logging

app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)


@app.route('/apiv1/user/<string:username>', methods=['GET'])
def getUserByUsername(username):
    # retrieves User record from users DB
    # returns JSON response containing user_id, username, email, password
    app.logger.info(f"Retrieving user for username: {username}")


    # UPDATE
    response = {'userId' : 1}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/apiv1/user', methods=['POST'])
def createUser():
    # creates new User record in users DB
    # request body should be JSON including username, email, password
    # returns JSON response containing user_id, username, email, password

    app.logger.info(f"Creating new user...")

    # UPDATE
    response = {'New User Info' : 'pretend info'}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/apiv1/tripGroup', methods=['POST'])
def addUserToTripGroup():
    # creates new record in trip_members DB to associate user with trip group
    # request body should be JSON including trip_id, user_id
    # returns response status 200 when successful
    app.logger.info(f"Adding user to trip group...")


    # UPDATE
    response = {'USER ADDED TO' : 'pretend group'}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/apiv1/tripGroup/<int:userId>', methods=['GET'])
def getTripsForUser(userId):
    # retrieves records from trip_members DB where user_id == userId
    # returns JSON response with all match records, including fields user_id and trip_id
    app.logger.info(f"Retrieving groups for user {userId}...")


    # UPDATE
    response = [{'user_id' : 1, 'trip_id': 1},{'user_id' : 1, 'trip_id': 3}]
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
app.run(host="0.0.0.0", port=4000)