## Trip Planner Service

The **Trip Planner Service** is a Flask application that implements the following routes to interface with the **Trip Planning Database** and **Object Store**:

1. /apiv1/trip [POST] - create new trip
2. /apiv1/trip/<tripId>/<date_string> [PATCH] - update an existing trip day by trip id and date
3. /apiv1/trip/<tripName> [GET] - retrieve trip overview info based on trip name
4. /apiv1/tripDays/<tripId> [GET] - retrieves all trip day records for specific tripId
5. /apiv1/addDocument [POST] - add trip document to object store


## Running Locally
### Connecting to Google Cloud Postgres SQL Database:

**Set environment variable GOOGLE_APPLICATION_CREDENTIALS via command:**

```export GOOGLE_APPLICATION_CREDENTIALS="path/to/db-serv-acc.json"```

Check value of environment variable via command:
```printenv GOOGLE_APPLICATION_CREDENTIALS```
