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

def testCreateUser():
    create_user_url = addr + f"/apiv1/user"
    headers = {'content-type': 'application/json'}

    data = jsonpickle.encode({ "username" : "New User",
                              "password" : "fakepassword",
                              "email" : "fakeemail@email.com"})

    response = requests.post(create_user_url, data=data, headers=headers)
    returnResp(response)

def testAddUserToGroup():
    create_group_url = addr + f"/apiv1/tripGroup"
    headers = {'content-type': 'application/json'}

    data = jsonpickle.encode({ "group" : "New User",
                              "user" : 1})

    response = requests.post(create_group_url, data=data, headers=headers)
    returnResp(response)
def testGetTripsForUser(userId):
    get_user_trips_url = addr + f"/apiv1/tripGroup/{userId}"
    headers = {'content-type': 'application/json'}

    response = requests.get(get_user_trips_url, headers=headers)
    returnResp(response)

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <cmd>")
    print(f"    where <cmd> is one of: getUser, createUser, addToGroup, getGroups")

else:

    cmd = sys.argv[1]

    if cmd == 'getUser':
        if (len(sys.argv) < 3):
            print(f"Usage: {sys.argv[0]} getUser <username>")
        else:
            print(f"Retrieving user information for user '{sys.argv[2]}'...")
            testGetUser(sys.argv[2])
    elif cmd == 'createUser':
        testCreateUser()
    elif cmd == 'addToGroup':
        testAddUserToGroup()
    elif cmd == 'getGroups':
        if (len(sys.argv) < 3):
            print(f"Usage: {sys.argv[0]} getGroups <userId>")
        else:
            print(f"Retrieving user information for user '{sys.argv[2]}'...")
            testGetTripsForUser(sys.argv[2])

    else:
        print("Unknown option", cmd)