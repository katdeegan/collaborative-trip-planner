#!/usr/bin/env python3

from flask import Flask, request, Response
import jsonpickle
import logging

app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)

@app.route('/apiv1/user/<int:id>', methods=['GET'])
def getUserById(id):
    app.logger.info(f"Retrieving user with ID: {id}")

    # UPDATE
    response = {'username' : 'pretend username'}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/apiv1/userId/<string:username>', methods=['GET'])
def getUserIdByUsername(username):
    app.logger.info(f"Retrieving ID for user: {username}")

    # UPDATE
    response = {'userId' : 1}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/apiv1/user', methods=['POST'])
def createUser():
    app.logger.info(f"Creating new user...")

    # UPDATE
    response = {'New User Info' : 'pretend info'}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/apiv1/group', methods=['POST'])
def createUserGroup():
    app.logger.info(f"Creating new group...")
    # user id in request body, associate this user with group

    # UPDATE
    response = {'USER ADDED TO' : 'pretend group'}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
app.run(host="0.0.0.0", port=4000)