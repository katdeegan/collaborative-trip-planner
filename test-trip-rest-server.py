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


def testCreateTrip():
    create_trip_url = addr + f"/apiv1/trip"
    headers = {'content-type': 'application/json'}

    data = jsonpickle.encode({ "trip_name" : "My trip",
                              "start_date" : "05-05-2025",
                              "end_date" : "05-15-2025",
                              "location" : "France"})

    response = requests.post(create_trip_url, data=data, headers=headers)
    returnResp(response)

def testUpdateTrip(id):
    update_trip_url = addr + f"/apiv1/trip/{id}"
    headers = {'content-type': 'application/json'}

    data = jsonpickle.encode({"location" : "Spain"})

    response = requests.patch(update_trip_url, data=data, headers=headers)
    returnResp(response)

def testGetTripId(group): 
    get_trip_id_url = addr + f"/apiv1/tripId/{group}"
    headers = {'content-type': 'application/json'}

    response = requests.get(get_trip_id_url, headers=headers)
    returnResp(response)

def testAddDoc(id):
    add_doc_url = addr + f"/apiv1/addDocument/{id}"
    headers = {'content-type': 'application/json'}

    data = jsonpickle.encode({ "tripId" : id,
                              "doc" : "encoded doc"})

    response = requests.post(add_doc_url, data=data, headers=headers)
    returnResp(response)

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <cmd>")
    print(f"    where <cmd> is one of: createTrip, updateTrip, getTripId, addDoc")

else:

    cmd = sys.argv[1]

    if cmd == 'createTrip':
        testCreateTrip()
    elif cmd == 'updateTrip':
        if (len(sys.argv) < 3):
            print(f"Usage: {sys.argv[0]} updateTrip <trip-id>")
        else:
            print(f"Updating trip with id {sys.argv[2]}...")
            testUpdateTrip(sys.argv[2])
    elif cmd == 'getTripId':
        if (len(sys.argv) < 3):
            print(f"Usage: {sys.argv[0]} getTripId <trip-name>")
        else:
            print(f"Retrieving trip ID for trip '{sys.argv[2]}'...")
            testGetTripId(sys.argv[2])
    elif cmd == 'addDoc':
        if (len(sys.argv) < 3):
            print(f"Usage: {sys.argv[0]} addDoc <trip-id>")
        else:
            print(f"Adding new trip document for trip with ID: {sys.argv[2]}...")
            testAddDoc(sys.argv[2])

    else:
        print("Unknown option", cmd)