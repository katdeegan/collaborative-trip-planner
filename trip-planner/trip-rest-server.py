#!/usr/bin/env python3

from flask import Flask, request, Response, jsonify
import jsonpickle
import logging
from google.cloud.sql.connector import Connector
import pg8000
import sqlalchemy
from sqlalchemy import text
from datetime import date, datetime
from sqlalchemy import create_engine, text

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

    try:
        request_data = request.get_json()
        trip_name = request_data.get("trip_name")
        start_date = request_data.get("start_date")
        end_date = request_data.get("end_date")

        # Validate input
        if not trip_name or not start_date or not end_date:
            error_resp = {'error': 'missing trip_name, start_date, or end_date'}
            return Response(response=jsonpickle.encode(error_resp), status=400, mimetype="application/json")

        # Insert and select queries for the trip_overview table
        insert_query = sqlalchemy.text(
            'INSERT INTO "trip_overview" (trip_name, start_date, end_date) VALUES (:trip_name, :start_date, :end_date);'
        )
        select_query = sqlalchemy.text(
            'SELECT * FROM "trip_overview" WHERE trip_name=:trip_name;'
        )
        with pool.connect() as db_conn:
            # Insert the new trip into the database
            db_conn.execute(insert_query, {
                "trip_name": trip_name,
                "start_date": start_date,
                "end_date": end_date
            })
            db_conn.commit()

            # Retrieve the inserted trip details
            result = db_conn.execute(select_query, {"trip_name": trip_name})

            # Convert the result to JSON format
            resp = [dict(zip(result.keys(), row)) for row in result.fetchall()]

            return Response(response=jsonpickle.encode(resp), status=201, mimetype="application/json")
    except Exception as e:
        # Handle any exceptions
        error_resp = {'error': str(e)}
        return Response(response=jsonpickle.encode(error_resp), status=500, mimetype="application/json")

@app.route('/apiv1/trip/<int:tripId>/<dateString>', methods=['PATCH'])
def updateTrip(tripId, dateString):
    # TODO fix 
    # UPDATE
    # updates field(s) for an existing trip day from trip_details DB
    # identifies record in DB by URL parameters: tripId, dateString
    # need to handle converting dateString into the appropiate type

    app.logger.info(f"Updating trip {tripId} for day {dateString}...")

    try:
        # Get JSON data from request
        request_data = request.get_json()
        if not request_data:
            return jsonify({"error": "No data provided"}), 400
        
        #app.logger.info(f"dateString: " + dateString)
        trip_date = datetime.strptime(dateString, "%m-%d-%Y").date()
        formatted_date = trip_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        app.logger.info(formatted_date)

        # TODO - how to get from 2001-01-02 form to 2000-01-01T00:00:00Z form as in table

        # Build the SQL update query dynamically
        fields_to_update = []
        for field, value in request_data.items():
            if field not in {"location", "accommodations", "travel", "activities", "dining", "notes"}:
                return jsonify({"error": f"Invalid field: {field}"}), 400
            fields_to_update.append(f"{field} = :{field}")
        
        if not fields_to_update:
            return jsonify({"error": "No valid fields to update"}), 400

        # Construct the UPDATE query
        update_query = sqlalchemy.text(f"""
            UPDATE trip_details
            SET {", ".join(fields_to_update)}
            WHERE trip_id = :trip_id AND date = :trip_date
        """)
        app.logger.info(update_query)

        
        reorder_query = sqlalchemy.text("""
            SELECT * FROM trip_details
            ORDER BY trip_id ASC, date ASC
        """)


        # Execute the query
        with pool.connect() as db_conn:
            result = db_conn.execute(update_query, {"trip_id": tripId, "trip_date": trip_date, **request_data})
            db_conn.execute(reorder_query)

            # Check if the record was updated
            if result.rowcount == 0:
                return jsonify({"error": "No matching record found"}), 404

        # Success response
        response = {'tripID': tripId, 'date': dateString, 'updatedFields': list(request_data.keys())}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")
    
    except ValueError:
        return jsonify({"error": "Invalid date format, expected YYYY-MM-DD"}), 400
    except Exception as e:
        app.logger.error(f"Error updating trip: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/apiv1/trip/<tripName>', methods=['GET'])
def getTrip(tripName): 
    # retrieves Trip record from trip_overview DB by tripName (trip name unique in database)
    # returns JSON response containing trip_id, trip_name, start_date, end_date
    app.logger.info(f"Retrieving trip overview information for trip '{tripName}'...")

    query = sqlalchemy.text('SELECT * FROM "trip_overview" WHERE trip_name = :tripname')

    with pool.connect() as db_conn:
        # retrieve trip overview 
        trip_overview_data = db_conn.execute(query, {"tripname":tripName})

        # converts response to json
        trip_resp = [dict(zip(trip_overview_data.keys(), row)) for row in trip_overview_data.fetchall()]

        # if no tripName is found
        if not trip_resp:
            error_resp = {'error': 'Trip not found', 'message': 'No trip data found for the given trip name.'}
            return Response(response=jsonpickle.encode(error_resp), status=404, mimetype="application/json")

        for row in trip_resp:
            for key, val in row.items():
                # convert date values to string in json response
                if isinstance(val, date):
                    row[key] = val.strftime('%Y-%m-%d')

        db_conn.commit()


        response_pickled = jsonpickle.encode(trip_resp[0])
        return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/apiv1/tripDays/<int:tripId>', methods=['GET'])
def getTripDayDetails(tripId):
    # retrieves all Trip Day records from trip_details DB with matching tripId
    # request body should include tripId
    # returns JSON response containing list of records, each record includes:
    # {trip_id, date, location, accommodation, travel, activities, dining, notes}

    app.logger.info(f"Retrieving trip day information for trip {tripId}...")

    try:
        # Query to retrieve all trip day records for the given tripId
        with pool.connect() as db_conn:
            query = text("""
                SELECT trip_id, date, location, accommodations, travel, activities, dining, notes
                FROM trip_details
                WHERE trip_id = :trip_id
            """)

            result = db_conn.execute(query, {"trip_id": tripId})

            # Fetch all rows from the result
            trip_days = result.fetchall()

            # If no records found, return a 404 error
            if not trip_days:
                return jsonify({"error": "No trip day records found for the given tripId"}), 404

            # Format the records into a list of dictionaries
            trip_day_list = [
                {
                    "trip_id": row[0],
                    "date": row[1].strftime('%Y-%m-%d') if isinstance(row[1], date) else None,
                    "location": row[2] if row[2] is not None else "N/A",
                    "accommodations": row[3] if row[3] is not None else "N/A",
                    "travel": row[4] if row[4] is not None else "N/A",
                    "activities": row[5] if row[5] is not None else "N/A",
                    "dining": row[6] if row[6] is not None else "N/A",
                    "notes": row[7] if row[7] is not None else "N/A"
                }
                for row in trip_days
            ]

        # Prepare the JSON response
        response_pickled = jsonpickle.encode({"tripDays": trip_day_list})
        return Response(response=response_pickled, status=200, mimetype="application/json")

    except Exception as e:
        app.logger.error(f"Error retrieving trip day details: {e}")
        return jsonify({"error": "Internal server error"}), 500
    

@app.route('/apiv1/addDocument/<int:tripId>', methods=['POST'])
def addDocument(tripId):
    app.logger.info(f"Adding trip document associated with trip {tripId} to object store...")
    # user id in request body, associate this user with group

    # UPDATE TODO
    response = {'Doc added' : 'successfully'}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
app.run(host="0.0.0.0", port=4000)