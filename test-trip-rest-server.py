import sys
import os
import base64
import jsonpickle, json
import requests

REST = os.getenv("REST") or "127.0.0.1:2000"
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

def testAddTripDay(tripId, tripDate):
    add_day_url = addr + f"/apiv1/tripDay"
    headers = {'content-type': 'application/json'}

    data = jsonpickle.encode({ "trip_id" : tripId,
                              "date" : tripDate})

    response = requests.post(add_day_url, data=data, headers=headers)
    returnResp(response)

def testUpdateTrip(id, date):
    update_trip_url = addr + f"/apiv1/trip/{id}/{date}"
    headers = {'content-type': 'application/json'}

    # TODO - how to pass do this via user input / frontend / CMD testing vs manually ?
    data = jsonpickle.encode({"location" : "France", "accommodations" : "Grand Plaza Hotel", "travel" : "bus", "last_updated_by": 1})

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

def testAddDoc(id, filepath):
    add_doc_url = addr + f"/apiv1/addDocument/{id}"
    headers = {'content-type': 'application/json'}

    data = jsonpickle.encode({ "tripId" : id,
                              "file" : filepath})

    response = requests.post(add_doc_url, data=data, headers=headers)
    returnResp(response)

def testGetTripDay(tripId, tripDate):
    get_trip_day_url = addr + f"/apiv1/tripDay/{tripId}/{tripDate}"
    headers = {'content-type': 'application/json'}

    response = requests.get(get_trip_day_url, headers=headers)
    returnResp(response)

def testDeleteTripDay(tripId, tripDate):
    delete_trip_day_url = addr + f"/apiv1/deleteTripDay/{tripId}/{tripDate}"
    headers = {'content-type': 'application/json'}
    response = requests.delete(delete_trip_day_url, headers=headers)
    returnResp(response)

def testGetDocs(tripId):
    get_docs_url = addr + f"/apiv1/getDocuments/{tripId}"
    headers = {'content-type': 'application/json'}

    response = requests.get(get_docs_url, headers=headers)
    returnResp(response)

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <cmd>")
    print(f"    where <cmd> is one of: createTrip, updateTrip, getTrip, getTripDays, addDoc")

else:

    cmd = sys.argv[1]

    if cmd == 'createTrip': # successfully works
        if (len(sys.argv) < 5):
            print(f"Usage: {sys.argv[0]} updateTrip <trip-name> <start-date> <end-date>")
        else:
            print(f"Creating trip '{sys.argv[2]}'...")
            testCreateTrip(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == 'updateTrip':  # works with json enconding hardcoded
        if (len(sys.argv) < 4):
            print(f"Usage: {sys.argv[0]} updateTrip <trip-id> <date>")
        else:
            print(f"Updating trip with id {sys.argv[2]} for day {sys.argv[3]}...")
            testUpdateTrip(sys.argv[2], sys.argv[3])
    elif cmd == 'getTrip': # successfully works 
        if (len(sys.argv) < 3):
            print(f"Usage: {sys.argv[0]} getTrip <trip-id>")
        else:
            print(f"Retrieving trip overview information for trip '{sys.argv[2]}'...")
            testGetTrip(sys.argv[2])
    elif cmd == 'getTripDays': # successfully works
        if (len(sys.argv) < 3):
            print(f"Usage: {sys.argv[0]} getTrip <trip-id>")
        else:
            print(f"Retrieving trip day information for trip {sys.argv[2]}...")
            testGetTripDays(sys.argv[2])
    elif cmd == 'getTripDay': 
        if (len(sys.argv) < 4):
            print(f"Usage: {sys.argv[0]} getTripDay <trip-id> <trip-date>")
        else:
            print(f"Retrieving info for Trip {sys.argv[2]} on Day {sys.argv[3]}...")
            testGetTripDay(sys.argv[2], sys.argv[3])
    elif cmd == 'deleteTripDay': 
        if (len(sys.argv) < 4):
            print(f"Usage: {sys.argv[0]} deleteTripDay <trip-id> <trip-date>")
        else:
            print(f"Deleting day {sys.argv[3]} from Trip {sys.argv[2]}...")
            testDeleteTripDay(sys.argv[2], sys.argv[3])
    
    elif cmd == 'addTripDay': 
        if (len(sys.argv) < 4):
            print(f"Usage: {sys.argv[0]} addTripDay <trip-id> <trip-date>")
        else:
            print(f"Adding day {sys.argv[3]} from Trip {sys.argv[2]}...")
            testAddTripDay(sys.argv[2], sys.argv[3])

    elif cmd == 'addDoc': # in progress
        if (len(sys.argv) < 3):
            print(f"Usage: {sys.argv[0]} addDoc <trip-id>")
        else:
            print(f"Adding new trip document for trip with ID {sys.argv[2]}, filepath {sys.argv[3]}")
            testAddDoc(sys.argv[2], sys.argv[3])
    
    elif cmd == "getDocs":
        if len(sys.argv) < 3:
            print(f"Usage: {sys.argv[0]} getDocs <trip-id>")
        else:
            print(f"Retrieving documents for trip with ID: {sys.argv[2]}...")
            testGetDocs(sys.argv[2])
    

    else:
        print("Unknown option", cmd)