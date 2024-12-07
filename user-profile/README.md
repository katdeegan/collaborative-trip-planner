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
