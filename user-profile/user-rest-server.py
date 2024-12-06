#!/usr/bin/env python3

from flask import Flask, request, Response, jsonify
import jsonpickle
import logging
from google.cloud.sql.connector import Connector
import pg8000
import sqlalchemy
from sqlalchemy import text
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS # for local testing - allow cross-origin requests (when frontend and backend are running on same machine on different ports)

app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)

CORS(app) 


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

def validateUserPassword(userId, userEnteredPassword):
    app.logger.info(f"Validating password for User {userId}...")
    query = sqlalchemy.text('SELECT password FROM "users" WHERE user_id = :userId')

    with pool.connect() as db_conn:
        user = db_conn.execute(query, {"userId":userId})
        if user is None:
                app.logger.warning(f"No user found with user_id: {userId}")
                return False
        
        json_resp = [dict(zip(user.keys(), row)) for row in user.fetchall()][0]

        user_password = json_resp['password']

        if userEnteredPassword == user_password:
            return True
        else:
            return False
        
def getUserByEmail(email):
    # retrieves User record from users DB by email
    # returns JSON response containing user_id, username, email, password
    app.logger.info(f"Retrieving user for email: {email}")

    query = sqlalchemy.text('SELECT * FROM "users" WHERE email = :email')

    with pool.connect() as db_conn:
        user = db_conn.execute(query, {"email":email})
        json_resp = [dict(zip(user.keys(), row)) for row in user.fetchall()][0]

        if not json_resp:
            error_resp = {'error': 'user not found', 'message': 'No user data found for the given email.'}
            return Response(response=jsonpickle.encode(error_resp), status=404, mimetype="application/json")
        
        response_pickled = jsonpickle.encode(json_resp)
        return Response(response=response_pickled, status=200, mimetype="application/json")


# 1. create new user in User Profile Database
@app.route('/apiv1/user', methods=['POST'])
def createUser():
    # creates new User record in users DB
    # request body should be JSON including username, email, password
    # returns JSON response containing user_id, username, email, password

    # TO-DO - return specific error message (and handle in frontend) when username or email is already used

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

# 2. retrieve user based on username
@app.route('/apiv1/user/<string:username>', methods=['GET'])
def getUserByUsername(username):
    # retrieves User record from users DB (username must be unique)
    # returns JSON response containing user_id, username, email, password
    app.logger.info(f"Retrieving user for username: {username}")

    query = sqlalchemy.text('SELECT * FROM "users" WHERE username = :username')

    with pool.connect() as db_conn:
        user = db_conn.execute(query, {"username":username})
        
        user_rows = user.fetchall()

        if not user_rows:
            error_resp = {'error': 'user not found', 'message': 'No user data found for the given username.'}
            return Response(response=jsonpickle.encode(error_resp), status=404, mimetype="application/json")
        
        json_resp = dict(zip(user.keys(), user_rows[0]))
        
        response_pickled = jsonpickle.encode(json_resp)
        return Response(response=response_pickled, status=200, mimetype="application/json")

# 3. associate a user with a trip group
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

# 4. retrieves all trips groups user is a part of
@app.route('/apiv1/tripGroup/<int:userId>', methods=['GET'])
def getTripsForUser(userId):
    # retrieves records from trip_members DB where user_id == userId
    # returns JSON string which is a list of trip_ids
    app.logger.info(f"Retrieving groups for user {userId}...")

    try:

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
            
            app.logger.info(f"Trips for User {userId}: {user_trips}")

            formatted_trip_ids = ', '.join(map(str, user_trips))
            trip_overview_query = f"SELECT trip_id, trip_name FROM trip_overview WHERE trip_id IN ({formatted_trip_ids})"

            user_trip_overview_data = db_conn.execute(sqlalchemy.text(trip_overview_query))

            app.logger.info(user_trip_overview_data)


            trip_resp = [dict(zip(user_trip_overview_data.keys(), row)) for row in user_trip_overview_data.fetchall()]

            return Response(response=jsonpickle.encode(trip_resp),status=200, mimetype="application/json")

    except Exception as e:
        error_resp = {'error': str(e)}
        return Response(response=jsonpickle.encode(error_resp), status=500, mimetype="application/json")
 
# 5. retrieves all users belonging to a specific trip
@app.route('/apiv1/tripUsers/<int:tripId>', methods=['GET'])
def getUsersForTrip(tripId):
    # returns list of users from given tripId
    # returns JSON string which is a list of user_ids
    app.logger.info(f"Retrieving users for trip {tripId}...")

    try:

        tripMembersQuery = sqlalchemy.text('SELECT user_id FROM "trip_members" WHERE trip_id = :tripId')
        #tripMembersQuery = sqlalchemy.text('SELECT user_id, username FROM "users" WHERE user_id = :userId')

        with pool.connect() as db_conn:

            user_trip_data = db_conn.execute(tripMembersQuery, {"tripId":tripId}).fetchall()

            # if trip has no users associated with them, return empty response
            if not user_trip_data:
                no_trips_resp = jsonpickle.encode([])
                return Response(response=no_trips_resp, status=200, mimetype="application/json")
            
            trip_users = []
            
            for user in user_trip_data:
                trip_users.append(user[0])
            
            app.logger.info(f"Users for Trip {tripId}: {trip_users}")

            formatted_user_ids = ', '.join(map(str, trip_users))
            tripMembersQuery = f"SELECT user_id, username FROM users WHERE user_id IN ({formatted_user_ids})"

            trip_user_data = db_conn.execute(sqlalchemy.text(tripMembersQuery))

            app.logger.info(trip_user_data)


            trip_resp = [dict(zip(trip_user_data.keys(), row)) for row in trip_user_data.fetchall()]

            return Response(response=jsonpickle.encode(trip_resp),status=200, mimetype="application/json")

    except Exception as e:
        error_resp = {'error': str(e)}
        return Response(response=jsonpickle.encode(error_resp), status=500, mimetype="application/json")
    
# 6. deletes a user from a trip
@app.route('/apiv1/deleteTripUser/<int:userId>/<int:tripId>', methods=['DELETE'])
def deleteTripUser(userId, tripId):
    selectQuery = f"SELECT * FROM trip_members WHERE trip_id={tripId} and user_id={userId}"
    deleteQuery = f"DELETE FROM trip_members WHERE trip_id={tripId} and user_id={userId}"
    try:
        with pool.connect() as db_conn:
            # check if record exists
            user_trip_data = db_conn.execute(sqlalchemy.text(selectQuery)).fetchall()
            app.logger.info(user_trip_data)
            if user_trip_data:
                # record found, now delete 
                db_conn.execute(sqlalchemy.text(deleteQuery)) 
                db_conn.commit() 
                
                return jsonify({"message": f"User {userId} has been deleted from trip {tripId}."}), 200
            else:
                return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 7. login a user
@app.route('/apiv1/login', methods=['POST'])
def loginUser():
    data = request.get_json()
    user = data.get("email_or_username")
    password = data.get("password")
    app.logger.info(f"Attempting to login {user}...")

    if not user or not password:
        error_resp = {"error" : "Missing email/username or password"}
        return Response(response=jsonpickle.encode(error_resp),status=400, mimetype="application/json")
        
    if '@' in user:
        # user attempting to login with email
        userRecord = getUserByEmail(user)
        app.logger.info(f"Successfully logged in user: {userRecord.get_json()}")
    else:
        # user attempting to login with username
        userRecord = getUserByUsername(user)
        app.logger.info(f"Successfully logged in user: {userRecord.get_json()}")
    
    if not userRecord:
        return Response(response=jsonpickle.encode({"error" : "Invalid username/email"}),status=401, mimetype="application/json")
    
    # validate password
    user_id = userRecord.get_json().get("user_id")
    username = userRecord.get_json().get("username")
    if validateUserPassword(user_id, password):
        app.logger.info(f"Login successful for User {user_id}!")
        #access_token = create_access_token(identity=user_id)
        json_resp = {"msg":"Login successful", "user_id":user_id, "username":username}
        return Response(response=jsonpickle.encode(json_resp), status=200, mimetype="application/json")
    else:
        return Response(response=jsonpickle.encode({"error" : "Invalid password"}),status=401, mimetype="application/json")
            

# start flask app
app.run(host="0.0.0.0", port=4000, debug=True)