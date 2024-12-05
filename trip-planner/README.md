## Trip Planner Service

The **Trip Planner Service** is a Flask application that implements the following routes to interface with the **Trip Planning Database** and **Object Store**:
```
1. /apiv1/trip [POST] - create new trip

2. /apiv1/trip/<tripId> [GET] - retrieve trip overview info based on trip ID

3. /apiv1/tripDays/<int:tripId> [GET] - retrieve all trip day records for specific tripId

4. /apiv1/tripDay/<int:tripId>/<tripDate> [GET] - retrieve all details for a specific day of a trip via tripId and tripDate

5. /apiv1/tripDay [POST] - add a day to the trip based on the tripId passed in the JSON body

6. /apiv1/deleteTripDay/<int:tripId>/<tripDate> [DELETE] - delete a day from a given trip by trip id and date of the day to delete

7. /apiv1/trip/<tripId>/<date_string> [PATCH] - update an existing trip day by trip id and date

8. /apiv1/addDocument/<int:tripId> [POST] - add trip document to object store for the given tripId

9. /apiv1/getDocuments/<int:tripId> [GET] - get all trip documents stored in the object bucket for the given tripId
 ```



## Running Locally
### Connecting to Google Cloud Postgres SQL Database:

**Set environment variable GOOGLE_APPLICATION_CREDENTIALS via command:**

```export GOOGLE_APPLICATION_CREDENTIALS="path/to/db-serv-acc.json"```

Check value of environment variable via command:
```printenv GOOGLE_APPLICATION_CREDENTIALS```
