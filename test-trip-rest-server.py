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


def testCreateTrip(tripName, startDate, endDate):
    # startDate and endDate in formate MM-DD-YYYY
    create_trip_url = addr + f"/apiv1/trip"
    headers = {'content-type': 'application/json'}

    data = jsonpickle.encode({ "trip_name" : tripName,
                              "start_date" : startDate,
                              "end_date" : endDate})

    response = requests.post(create_trip_url, data=data, headers=headers)
    returnResp(response)

def testUpdateTrip(id, date):
    update_trip_url = addr + f"/apiv1/trip/{id}/{date}"
    headers = {'content-type': 'application/json'}

    data = jsonpickle.encode({"location" : "Spain"})

    response = requests.patch(update_trip_url, data=data, headers=headers)
    returnResp(response)

def testGetTrip(tripName): 
    get_trip_id_url = addr + f"/apiv1/trip/{tripName}"
    headers = {'content-type': 'application/json'}

    response = requests.get(get_trip_id_url, headers=headers)
    returnResp(response)

def testGetTripDays(tripId): 
    get_trip_days_id_url = addr + f"/apiv1/tripDays/{tripId}"
    headers = {'content-type': 'application/json'}

    response = requests.get(get_trip_days_id_url, headers=headers)
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
    print(f"    where <cmd> is one of: createTrip, updateTrip, getTrip, getTripDays, addDoc")

else:

    cmd = sys.argv[1]

    if cmd == 'createTrip':
        if (len(sys.argv) < 5):
            print(f"Usage: {sys.argv[0]} updateTrip <trip-name> <start-date> <end-date>")
        else:
            print(f"Creating trip '{sys.argv[2]}'...")
            testCreateTrip(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == 'updateTrip':
        if (len(sys.argv) < 4):
            print(f"Usage: {sys.argv[0]} updateTrip <trip-id> <date>")
        else:
            print(f"Updating trip with id {sys.argv[2]} for day {sys.argv[3]}...")
            testUpdateTrip(sys.argv[2], sys.argv[3])
    elif cmd == 'getTrip':
        if (len(sys.argv) < 3):
            print(f"Usage: {sys.argv[0]} getTrip <trip-name>")
        else:
            print(f"Retrieving trip overview information for trip '{sys.argv[2]}'...")
            testGetTrip(sys.argv[2])
    elif cmd == 'getTripDays':
        if (len(sys.argv) < 3):
            print(f"Usage: {sys.argv[0]} getTrip <trip-id>")
        else:
            print(f"Retrieving trip day information for trip {sys.argv[2]}...")
            testGetTripDays(sys.argv[2])
    elif cmd == 'addDoc':
        if (len(sys.argv) < 3):
            print(f"Usage: {sys.argv[0]} addDoc <trip-id>")
        else:
            print(f"Adding new trip document for trip with ID: {sys.argv[2]}...")
            testAddDoc(sys.argv[2])

    else:
        print("Unknown option", cmd)