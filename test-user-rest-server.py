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


def testGetUser(id):
    get_user_url = addr + f"/apiv1/user/{id}"
    headers = {'content-type': 'application/json'}

    response = requests.get(get_user_url, headers=headers)
    returnResp(response)

def testGetUserId(username):
    get_user_id_url = addr + f"/apiv1/userId/{username}"
    headers = {'content-type': 'application/json'}

    response = requests.get(get_user_id_url, headers=headers)
    returnResp(response)

def testCreateUser():
    create_user_url = addr + f"/apiv1/user"
    headers = {'content-type': 'application/json'}

    data = jsonpickle.encode({ "username" : "New User",
                              "password" : "fakepassword",
                              "email" : "fakeemail@email.com"})

    response = requests.post(create_user_url, data=data, headers=headers)
    returnResp(response)

def testCreateGroup():
    create_group_url = addr + f"/apiv1/group"
    headers = {'content-type': 'application/json'}

    data = jsonpickle.encode({ "group" : "New User",
                              "user" : 1})

    response = requests.post(create_group_url, data=data, headers=headers)
    returnResp(response)

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <cmd>")
    print(f"    where <cmd> is one of: getUser, getUserId, createUser, createGroup")

else:

    cmd = sys.argv[1]

    if cmd == 'getUser':
        if (len(sys.argv) < 3):
            print(f"Usage: {sys.argv[0]} getUser <id>")
        else:
            print(f"Retrieving user with id {sys.argv[2]}...")
            testGetUser(sys.argv[2])
    elif cmd == 'getUserId':
        if (len(sys.argv) < 3):
            print(f"Usage: {sys.argv[0]} getUser <username>")
        else:
            print(f"Retrieving user ID for {sys.argv[2]}...")
            testGetUserId(sys.argv[2])
    elif cmd == 'createUser':
        testCreateUser()
    elif cmd == 'createGroup':
        testCreateGroup()

    else:
        print("Unknown option", cmd)