## User Profile Service

The **User Profile Service** is a Flask application that implements the following routes to interface with the **User Profile Database**:

1. /apiv1/user/<id> [GET] - retrieve user profile information based on user ID
2. /apiv1/userId/<username> [GET] - retrieve user id based on username
3. /apiv1/user [POST] - create new user in **User Profile Database**
4. /apiv1/group [POST] - create new trip group / associate a user with a new trip group