## User Profile Service

The **User Profile Service** is a Flask application that implements the following routes to interface with the **User Profile Database**:

1. /apiv1/user/<username> [GET] - retrieve user based on username
2. /apiv1/user [POST] - create new user in **User Profile Database**
3. /apiv1/tripGroup [POST] - associate a user with a trip group
4. /apiv1/tripGroup [GET] - retrieves all trips groups user is a part of