#!/usr/bin/env python3

from flask import Flask, request, Response, jsonify
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


@app.route('/apiv1/user/<string:username>', methods=['GET'])
def getUserByUsername(username):
    # retrieves User record from users DB (username must be unique)
    # returns JSON response containing user_id, username, email, password
    app.logger.info(f"Retrieving user for username: {username}")

    query = sqlalchemy.text('SELECT * FROM "users" WHERE username = :username')

    with pool.connect() as db_conn:
        user = db_conn.execute(query, {"username":username})

        if not user:
            error_resp = {'error': 'user not found', 'message': 'No user data found for the given username.'}
            return Response(response=jsonpickle.encode(error_resp), status=404, mimetype="application/json")

        json_resp = [dict(zip(user.keys(), row)) for row in user.fetchall()]
        
    response_pickled = jsonpickle.encode(json_resp)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/apiv1/user', methods=['POST'])
def createUser():
    # creates new User record in users DB
    # request body should be JSON including username, email, password
    # returns JSON response containing user_id, username, email, password

    app.logger.info(f"Creating new user...")

    try:
        request_data = request.get_json()
        username = request_data.get("username")
        email = request_data.get("email")
        password = request_data.get("password")


        if not username or not email or not password:
            error_resp = {'error': 'missing username, password or email'}
            return Response(response=jsonpickle.encode(error_resp), status=400, mimetype="application/json")

        # user database has unique constraint on username
        insert_query = sqlalchemy.text('INSERT INTO "users" (username, email, password) VALUES (:username, :email, :password);')
        select_query = sqlalchemy.text('SELECT * FROM "users" where username=:username;')

        with pool.connect() as db_conn:
            db_conn.execute(insert_query, {"username":username, "email":email, "password":password})
            db_conn.commit()
            result = db_conn.execute(select_query, {"username":username})

            # converts response to json
            resp = [dict(zip(result.keys(), row)) for row in result.fetchall()]

            return Response(response=jsonpickle.encode(resp),status=201, mimetype="application/json")
    except Exception as e:
        error_resp = {'error': str(e)}
        return Response(response=jsonpickle.encode(error_resp), status=500, mimetype="application/json")
    
@app.route('/apiv1/tripGroup', methods=['POST'])
def addUserToTripGroup():
    # creates new record in trip_members DB to associate user with trip group
    # request body should be JSON including trip_id, user_id
    # returns response status 200 when successful
    app.logger.info(f"Adding user to trip group...")

    # TODO - somewhere in app logic, need to verify userId and tripId exist

    try:
        request_data = request.get_json()
        userId = request_data.get("user_id")
        tripId = request_data.get("trip_id")

        if not userId or not tripId:
            error_resp = {'error': 'missing trip_id or user_id'}
            return Response(response=jsonpickle.encode(error_resp), status=400, mimetype="application/json")


        insert_query = sqlalchemy.text('INSERT INTO "trip_members" (user_id, trip_id) VALUES (:userId, :tripId);')
        select_query = sqlalchemy.text('SELECT * FROM "trip_members" where user_id=:userId and trip_id=:tripId;')

        with pool.connect() as db_conn:
            db_conn.execute(insert_query, {"userId":userId, "tripId":tripId})
            db_conn.commit()
            result = db_conn.execute(select_query, {"userId":userId, "tripId":tripId})

            # converts response to json
            trip_resp = [dict(zip(result.keys(), row)) for row in result.fetchall()]

            return Response(response=jsonpickle.encode(trip_resp),status=201, mimetype="application/json")
    except Exception as e:
        error_resp = {'error': str(e)}
        return Response(response=jsonpickle.encode(error_resp), status=500, mimetype="application/json")

@app.route('/apiv1/tripGroup/<int:userId>', methods=['GET'])
def getTripsForUser(userId):
    # retrieves records from trip_members DB where user_id == userId
    # returns JSON string which is a list of trip_ids
    app.logger.info(f"Retrieving groups for user {userId}...")

    query = sqlalchemy.text('SELECT trip_id FROM "trip_members" WHERE user_id = :userId')

    with pool.connect() as db_conn:

        user_trip_data = db_conn.execute(query, {"userId":userId}).fetchall()

        # if user has no trips associated with them, return empty response
        if not user_trip_data:
            no_trips_resp = jsonpickle.encode([])
            return Response(response=no_trips_resp, status=200, mimetype="application/json")
        
        user_trips = []
        
        for trip in user_trip_data:
            user_trips.append(trip[0])

        json_resp = jsonpickle.encode(user_trips)

        return Response(response=json_resp, status=200, mimetype="application/json")


# start flask app
app.run(host="0.0.0.0", port=4000)