## Messaging - Email Alerts Service

The **Email Alerts Service** is a Python application that monitors a message queue in **Redis**. Messages are added to the Redis queue when the **trip_details** table in the **Trip Planning Postgres SQL Database** is updated (i.e. a trip member updates the itinerary on one of the trip days).

Once the Redis message is dequeued, the **Email Alerts Service** sends an email to all members of the trip, informing them of who made the chage and to what day (date) of the trip the change was made to.

## Running Locally
### Connecting to Google Cloud Postgres SQL Database:

**Set environment variable GOOGLE_APPLICATION_CREDENTIALS via command:**

```export GOOGLE_APPLICATION_CREDENTIALS="path/to/db-serv-acc.json"```

Check value of environment variable via command:
```printenv GOOGLE_APPLICATION_CREDENTIALS```
