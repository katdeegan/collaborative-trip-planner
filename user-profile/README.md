## User Profile Service

The **User Profile Service** is a Flask application that implements the following routes to interface with the **User Profile Database**:
```
1. /apiv1/user [POST] - create new user in User Profile Database

2. /apiv1/user/<username> [GET] - retrieve user based on username

3. /apiv1/tripGroup [POST] - associate a user with a trip group

4. /apiv1/tripGroup/<userId> [GET] - retrieves all trips groups user is a part of

5. /apiv1/tripUsers/<tripId> [GET] - retrieves all users belonging to a specific trip

6. apiv1/deleteTripUser/<userId>/<tripId> [DELETE] - deletes a user from a trip

7. /apiv1/login [POST] - login a user

```

## Running Locally
### Connecting to Google Cloud Postgres SQL Database:

**Set environment variable GOOGLE_APPLICATION_CREDENTIALS via command:**

```export GOOGLE_APPLICATION_CREDENTIALS="path/to/db-serv-acc.json"```

Check value of environment variable via command:
```printenv GOOGLE_APPLICATION_CREDENTIALS```

## Testing endpoints

The **test-user-rest-server.py** file (located in the root project directory) can be used to test each of the routes described above. This file assumes you are runnning the server locally and the REST variable in the script will need to be updated if you are running the server elsewhere.

Run the test script via the terminal command:

```python3 test-user-rest-server.py <CMD> [params]```

Accepted **CMD** arguments include: **getUser, createUser, addToGroup, getGroups, getUsers, login, deleteTripUser**

## Deploying to Kubernetes

To run this service on a pod in a Kubernetes cluster, excute the following terminal commands:

```bash
kubectl apply -f user-profile/deployment.yaml

kubectl apply -f user-profile/service.yaml
```

As configured, these commands will provision a Kubernetes pod to host the user rest server (number of pods can be scaled based on application needs), and a Load Balancer service so that the pod(s) may be access either by service name (from within Kubernetes cluster) or externally (via **EXTERNAL_IP**).


