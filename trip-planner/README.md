## Trip Planner Service

The **Trip Planner Service** is a Flask application that implements the following routes to interface with the **Trip Planning Database** and **Object Store**:
```
1. /apiv1/trip [POST] - create new trip

2. /apiv1/trip/<tripId> [GET] - retrieve trip overview info based on trip ID

3. /apiv1/tripDays/<tripId> [GET] - retrieve all trip day records for specific tripId

4. /apiv1/tripDay/<tripId>/<tripDate> [GET] - retrieve all details for a specific day of a trip via tripId and tripDate

5. /apiv1/tripDay [POST] - add a day to the trip based on the tripId passed in the JSON body

6. /apiv1/deleteTripDay/<tripId>/<tripDate> [DELETE] - delete a day from a given trip by trip id and date of the day to delete

7. /apiv1/trip/<tripId>/<date_string> [PATCH] - update an existing trip day by trip id and date. Route also adds a message to Redis queue (includes information on what trip was updated, what user performed the update, and what trip date was updated) after successfully patching the trip-details record.s

8. /apiv1/addDocument/<tripId> [POST] - add trip document to object store for the given tripId

9. /apiv1/getDocuments/<tripId> [GET] - get all trip documents stored in the object bucket for the given tripId
 ```



## Running Locally
### Connecting to Google Cloud Postgres SQL Database:

**Set environment variable GOOGLE_APPLICATION_CREDENTIALS via command:**

```export GOOGLE_APPLICATION_CREDENTIALS="path/to/db-serv-acc.json"```

Check value of environment variable via command:
```printenv GOOGLE_APPLICATION_CREDENTIALS```

## Testing endpoints

The **test-trip-rest-server.py** file (located in the root project directory) can be used to test each of the routes described above. This file assumes you are runnning the server locally and the REST variable in the script will need to be updated if you are running the server elsewhere.

Run the test script via the terminal command:

```python3 test-trip-rest-server.py <CMD> [params]```

Accepted **CMD** arguments include: **createTrip, updateTrip, getTrip, getTripDays, getTripDay, deleteTripDay, addTripDay, addDoc, getDocs**

## Deploying to Kubernetes

To run this service on a pod in a Kubernetes cluster, excute the following terminal commands:

```bash
kubectl apply -f trip-planner/deployment.yaml

kubectl apply -f trip-planner/service.yaml
```

As configured, these commands will provision a Kubernetes pod to host the trip rest server (number of pods can be scaled based on application needs), and a Load Balancer service so that the pod(s) may be access either by service name (from within Kubernetes cluster) or externally (via **EXTERNAL_IP**).

