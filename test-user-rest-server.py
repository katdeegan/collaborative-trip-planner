import sys
import os
import base64
import jsonpickle, json
import requests

REST = os.getenv("REST") or "127.0.0.1:4000"
addr = f"http://{REST}"

def returnResp(response):
    if response.status_code == 200:
        jsonResponse = json.dumps(response.json(), indent=4, sort_keys=True)
        print(jsonResponse)
        return
    else:
        print(
            f"response code is {response.status_code}, raw response is {response.text}")
        return response.text


def testGetUser(username):
    get_user_url = addr + f"/apiv1/user/{username}"
    headers = {'content-type': 'application/json'}

    response = requests.get(get_user_url, headers=headers)
    returnResp(response)

def testCreateUser(username, email, password):
    create_user_url = addr + f"/apiv1/user"
    headers = {'content-type': 'application/json'}

    data = jsonpickle.encode({ "username" : username,
                              "password" : password,
                              "email" : email})

    response = requests.post(create_user_url, data=data, headers=headers)
    returnResp(response)

def testAddUserToGroup(userId, tripId):
    create_group_url = addr + f"/apiv1/tripGroup"
    headers = {'content-type': 'application/json'}

    data = jsonpickle.encode({ "user_id" : userId,
                              "trip_id" : tripId})

    response = requests.post(create_group_url, data=data, headers=headers)
    returnResp(response)
def testGetTripsForUser(userId):
    get_user_trips_url = addr + f"/apiv1/tripGroup/{userId}"
    headers = {'content-type': 'application/json'}

    response = requests.get(get_user_trips_url, headers=headers)
    returnResp(response)
<<<<<<< HEAD

def testLoginUser(user, password):
    login_user_url = addr + f"/apiv1/login"
    headers = {'content-type': 'application/json'}
    data = jsonpickle.encode({ "email_or_username" : user,
                              "password" : password})
    response = requests.post(login_user_url, data=data, headers=headers)
    returnResp(response)

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <cmd>")
    print(f"    where <cmd> is one of: getUser, createUser, addToGroup, getGroups, login")
=======

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <cmd>")
    print(f"    where <cmd> is one of: getUser, createUser, addToGroup, getGroups")
>>>>>>> ebef2826be125fdbb04d886d282e4173a796357a

else:

    cmd = sys.argv[1]

    if cmd == 'getUser':
        if (len(sys.argv) < 3):
            print(f"Usage: {sys.argv[0]} getUser <username>")
        else:
            print(f"Retrieving user information for user '{sys.argv[2]}'...")
            testGetUser(sys.argv[2])
    elif cmd == 'createUser':
        if (len(sys.argv) < 5):
            print(f"Usage: {sys.argv[0]} createUser <username> <email> <password>")
        else:
            print(f"Creating user {sys.argv[2]}...")
            testCreateUser(sys.argv[2],sys.argv[3],sys.argv[4])
    elif cmd == 'addToGroup':
        if (len(sys.argv) < 4):
            print(f"Usage: {sys.argv[0]} addToGroup <userId> <tripId>")
        else:
            print(f"Adding user {sys.argv[2]} to trip {sys.argv[3]}...")
            testAddUserToGroup(sys.argv[2],sys.argv[3])
    elif cmd == 'getGroups':
        if (len(sys.argv) < 3):
            print(f"Usage: {sys.argv[0]} getGroups <userId>")
        else:
            print(f"Retrieving user information for user {sys.argv[2]}...")
            testGetTripsForUser(sys.argv[2])
<<<<<<< HEAD
    elif cmd == 'login':
        if (len(sys.argv) < 4):
            print(f"Usage: {sys.argv[0]} login <username or email> <password>")
        else:
            print(f"Retrieving user information for user {sys.argv[2]}...")
            testLoginUser(sys.argv[2], sys.argv[3])
=======
>>>>>>> ebef2826be125fdbb04d886d282e4173a796357a

    else:
        print("Unknown option", cmd)