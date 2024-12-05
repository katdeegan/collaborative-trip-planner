#!/usr/bin/env python3

from flask import Flask, request, Response, jsonify
import jsonpickle
import logging
from google.cloud.sql.connector import Connector
import pg8000
import sqlalchemy
from sqlalchemy import text
from datetime import date, datetime
import datetime
from google.cloud import storage
from flask_cors import CORS # for local testing - allow cross-origin requests (when frontend and backend are running on same machine on different ports)

app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)

CORS(app) 

# initialize Connector object
connector = Connector()

# Initialize GCS client for doc storage
storage_client = storage.Client()
bucket_name = "trip-planner-docs"  

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

@app.route('/apiv1/tripDay/<int:tripId>/<tripDate>', methods=['GET'])
def getTripDayDetails(tripId, tripDate):
    try:
        with pool.connect() as db_conn:
            query = f"SELECT * FROM trip_details WHERE trip_id={tripId} and date='{tripDate}'"
            tripDayResult = db_conn.execute(sqlalchemy.text(query))

            row = tripDayResult.fetchall()[0]
            if not row:
                error_resp = {'error': 'trip day not found'}
                return Response(response=jsonpickle.encode(error_resp), status=404, mimetype="application/json")
        
            trip_day_list = {
                    "trip_id": row[0],
                    "date": row[1].strftime('%Y-%m-%d') if isinstance(row[1], date) else None,
                    "location": row[2] if row[2] is not None else "N/A",
                    "accommodations": row[3] if row[3] is not None else "N/A",
                    "travel": row[4] if row[4] is not None else "N/A",
                    "activities": row[5] if row[5] is not None else "N/A",
                    "dining": row[6] if row[6] is not None else "N/A",
                    "notes": row[7] if row[7] is not None else "N/A"
                }
            

            app.logger.info(f"trip day: {trip_day_list}")

            response_pickled = jsonpickle.encode(trip_day_list)
            return Response(response=response_pickled, status=200, mimetype="application/json")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/apiv1/deleteTripDay/<int:tripId>/<tripDate>', methods=['DELETE'])
def deleteTripDay(tripId, tripDate):
    # delete trip day using id + date
    app.logger.info(f"Deleting trip day {tripDate} to Trip {tripId}")
    
    selectQuery = f"SELECT * FROM trip_details WHERE trip_id={tripId} and date='{tripDate}'"
    deleteQuery = f"DELETE FROM trip_details WHERE trip_id={tripId} and date='{tripDate}'"
    try:
        with pool.connect() as db_conn:
            # check if record exists
            select_result = db_conn.execute(sqlalchemy.text(selectQuery)).fetchall()
            app.logger.info(select_result)
            if select_result:
                # record found, now delete 
                db_conn.execute(sqlalchemy.text(deleteQuery)) 
                db_conn.commit() 
                
                return jsonify({"message": f"Trip day {tripDate} has been deleted from trip {tripId}."}), 200
            else:
                return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/apiv1/tripDay', methods=['POST'])
def addTripDay():
    try:
        request_data = request.get_json()
        tripId = request_data.get("trip_id")
        tripDate = request_data.get("date")
        app.logger.info(f"Adding trip day {tripDate} to Trip {tripId}")

        if not tripId or not tripDate:
            error_resp = {'error': 'missing trip_id, or date'}
            return Response(response=jsonpickle.encode(error_resp), status=400, mimetype="application/json")
        
        insert_query = f"INSERT INTO trip_details (trip_id, date) VALUES ({tripId}, '{tripDate}');"
        select_query = f"SELECT * FROM trip_details where trip_id={tripId} and date='{tripDate}';"

        with pool.connect() as db_conn:
            app.logger.info("Inserting trip day...")
            db_conn.execute(sqlalchemy.text(insert_query))
            db_conn.commit()
            app.logger.info("Fetching trip day...")
            result = db_conn.execute(sqlalchemy.text(select_query))
            trip_resp = [dict(zip(result.keys(), row)) for row in result.fetchall()]
            return Response(response=jsonpickle.encode(trip_resp),status=201, mimetype="application/json")
    except Exception as e:
        error_resp = {'error': str(e)}
        return Response(response=jsonpickle.encode(error_resp), status=500, mimetype="application/json")

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
        check_query = sqlalchemy.text(
            'SELECT COUNT(*) FROM "trip_overview" WHERE trip_name = :trip_name;'
        )
        with pool.connect() as db_conn:
            # Check if trip_name already exists
            existing = db_conn.execute(check_query, {"trip_name": trip_name}).scalar()
            if existing > 0:
                error_resp = {'error': f'Trip with name "{trip_name}" already exists'}
                return Response(response=jsonpickle.encode(error_resp), status=409, mimetype="application/json")

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
            # resp = [dict(zip(result.keys(), row)) for row in result.fetchall()]

            resp = []
            for row in result.fetchall():
                row_dict = dict(zip(result.keys(), row))
                
                # Safely format the date fields
                start_date = row_dict.get("start_date")
                end_date = row_dict.get("end_date")
                
                if isinstance(start_date, (datetime.date, datetime.datetime)):
                    row_dict["start_date"] = start_date.strftime("%Y-%m-%d")
                if isinstance(end_date, (datetime.date, datetime.datetime)):
                    row_dict["end_date"] = end_date.strftime("%Y-%m-%d")
                
                resp.append(row_dict)

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
        
        app.logger.info(request_data)

        trip_date = dateString
        new_trip_date = trip_date
        '''
        try:
            trip_date = datetime.datetime.strptime(dateString, "%m-%d-%Y").date()
        except ValueError:
            trip_date = datetime.datetime.strptime(dateString, "%Y-%m-%d").date()
        '''
        #formatted_date = trip_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        app.logger.info(f"Original Trip Date: {trip_date}")

        # TODO - check that date and trip are valid (exist and in range)

        # Build the SQL update query dynamically
        fields_to_update = []
        for field, value in request_data.items():
            if field not in {"location", "accommodations", "travel", "activities", "dining", "notes", "date", "last_updated_by"}:
                return jsonify({"error": f"Invalid field: {field}"}), 400
            if field == "date":
                new_trip_date = request_data["date"]
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
            db_conn.commit()

            # Check if the record was updated
            if result.rowcount == 0:
                return jsonify({"error": "No matching record found"}), 404

        # Success response
        response = {'tripID': tripId, 'date': new_trip_date, 'updatedFields': list(request_data.keys())}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")
    
    except ValueError:
        return jsonify({"error": "Invalid date format, expected MM-DD-YYYY or YYYY-MM-DD"}), 400
    except Exception as e:
        app.logger.error(f"Error updating trip: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/apiv1/trip/<tripId>', methods=['GET'])
def getTrip(tripId): 
    # retrieves Trip record from trip_overview DB by tripName (trip name unique in database)
    # returns JSON response containing trip_id, trip_name, start_date, end_date
    app.logger.info(f"Retrieving trip overview information for trip '{tripId}'...")

    query = sqlalchemy.text('SELECT * FROM "trip_overview" WHERE trip_id = :tripId')

    with pool.connect() as db_conn:
        # retrieve trip overview 
        trip_overview_data = db_conn.execute(query, {"tripId":tripId})

        # converts response to json
        trip_resp = [dict(zip(trip_overview_data.keys(), row)) for row in trip_overview_data.fetchall()]

        # if no tripName is found
        if not trip_resp:
            error_resp = {'error': 'Trip not found', 'message': 'No trip data found for the given trip ID.'}
            return Response(response=jsonpickle.encode(error_resp), status=404, mimetype="application/json")

        for row in trip_resp:
            for key, val in row.items():
                # convert date values to string in json response
                if isinstance(val, date):
                    row[key] = val.strftime('%Y-%m-%d')

        # db_conn.commit() # TODO - not needed ?


        response_pickled = jsonpickle.encode(trip_resp[0])
        return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/apiv1/tripDays/<int:tripId>', methods=['GET'])
def getTripDaysDetails(tripId):
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
    # user id in request body, associate this user with group # TODO

# TODO
    try:
        app.logger.info(f"getting file from the request...")
        # Get the file from the request
        file = request.files['file']  # Assume file is sent as form-data in the 'file' field
        app.logger.info(f"file received from request...")
        if not file:
            return jsonify({"error": "No file provided"}), 400

        # Get the file content and prepare the blob name (could be based on tripId or file name)
        blob_name = f"trip_documents/{tripId}/{file.filename}"
        app.logger.info(f"Blob_name: {blob_name} ")
        
        # Upload the file to Google Cloud Storage
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_file(file)

        app.logger.info(f"File uploaded to {blob_name} in GCS")

        # Respond with success
        response = {'Doc added': 'successfully'}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")

    except Exception as e:
        app.logger.error(f"Error uploading file: {str(e)}")
        return jsonify({"error": f"Error uploading file: {str(e)}"}), 500


# start flask app
app.run(host="0.0.0.0", port=2000)