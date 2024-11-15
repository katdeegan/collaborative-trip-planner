## Trip Planner Service

The **Trip Planner Service** is a Flask application that implements the following routes to interface with the **Trip Planning Database** and **Object Store**:

1. /apiv1/trip [POST] - create new trip in database (trip is associated with an existing trip group)
2. /apiv1/trip/<id> [PATCH] - update an existing trip
3. /apiv1/tripId/<group> [GET] - retrieve trip is of a specific trip group
4. /apiv1/addDocument [POST] - add trip document to object store