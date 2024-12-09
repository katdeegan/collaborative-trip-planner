import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from google.cloud.sql.connector import Connector
import redis
import os
import sqlalchemy
from sqlalchemy import text
from datetime import datetime

connector = Connector()

# function to return the database connection
def getconn():
    conn = connector.connect(
        "trip-planner-442220:us-central1:trip-planner-db",
        "pg8000",
        user="postgres",
        password="TripPl4nn3r!",
        db="postgres"
    )
    return conn

# create connection pool
pool = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

# Test the connection
with pool.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print(result.fetchone())

# connect to Redis
redis_host = os.getenv('REDIS_HOST') or '35.193.96.145'

# Connect to Redis
r = redis.Redis(host=redis_host, port=6379, db=0)

print(redis_host)

redis_queue = "tripUpdated"

# Function to send email
def send_email_org(subject, body, to_emails, smtp_server, smtp_port, sender_email, sender_password, attachment=None):
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ', '.join(to_emails)  # List of recipient emails
        msg['Subject'] = subject
        
        # Attach the body content
        msg.attach(MIMEText(body, 'plain'))

        # Attach file if provided
        if attachment:
            with open(attachment, 'rb') as file:
                part = MIMEApplication(file.read(), Name=attachment)
                part['Content-Disposition'] = f'attachment; filename="{attachment}"'
                msg.attach(part)

        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)  # Log in to the SMTP server
            text = msg.as_string()  # Convert message to string
            server.sendmail(sender_email, to_emails, text)  # Send email

        print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {str(e)}")

# List of recipient emails
recipient_list = ['katdeegan16@gmail.com', 'katdeegan16@att.net']

# Email details
subject = "Test Email"
body = "This is a test email sent from Python!"
sender_email = "collaborativetripplanner@gmail.com"
sender_password = "fhqj mkxb imis qfnq"  # It's recommended to use environment variables or app passwords for security
smtp_server = "smtp.gmail.com"  # For Gmail
smtp_port = 587  # Port for TLS

# Optional: file attachment path
attachment = None  # If you have a file to attach, otherwise set to None

# Send the email
#xsend_email(subject, body, recipient_list, smtp_server, smtp_port, sender_email, sender_password, attachment)

def format_date(date_string):
    date_obj = datetime.strptime(date_string, "%Y-%m-%d")
    return date_obj.strftime("%B %d, %Y")


def get_trip_members_emails(trip_id):
    # returns list of trip member email addresses
    try:
        tripMembersIdQuery = sqlalchemy.text('SELECT user_id FROM "trip_members" WHERE trip_id = :tripId')
        with pool.connect() as db_conn:
            user_trip_data = db_conn.execute(tripMembersIdQuery, {"tripId":trip_id}).fetchall()

            # if trip has no users associated with them, return empty response
            if not user_trip_data:
                return []
            
            trip_users = []
            
            for user in user_trip_data:
                trip_users.append(user[0])
            
            print(f"Users for Trip {trip_id}: {trip_users}")

            formatted_user_ids = ', '.join(map(str, trip_users))
            tripMembersQuery = f"SELECT email FROM users WHERE user_id IN ({formatted_user_ids})"

            trip_member_emails = db_conn.execute(sqlalchemy.text(tripMembersQuery)).fetchall()

            print(f"Emails for Trip members: {trip_member_emails}")

            trip_emails = []

            for email in trip_member_emails:
                trip_emails.append(email[0])
            
            return trip_emails
    
    except Exception as e:
        print("Error retrieving trip member information")
        return []

def get_trip_name(trip_id):
    # returns trip name
    query = sqlalchemy.text('SELECT trip_name FROM "trip_overview" WHERE trip_id = :tripId')
    with pool.connect() as db_conn:
        trip_overview_data = db_conn.execute(query, {"tripId":trip_id})
        trip_resp = [dict(zip(trip_overview_data.keys(), row)) for row in trip_overview_data.fetchall()]

        # if no tripName is found
        if not trip_resp:
            print("No trip name found")
            return ""
        
        return trip_resp[0]["trip_name"]

def get_user_who_updated(user_id):
    # returns name of user
    query = sqlalchemy.text('SELECT username FROM "users" WHERE user_id = :userId')

    with pool.connect() as db_conn:
        user_data = db_conn.execute(query, {"userId":user_id})
        user_resp = [dict(zip(user_data.keys(), row)) for row in user_data.fetchall()]

        if not user_resp:
            print("No user found")
            return ""
        
        return user_resp[0]["username"]


def send_email(emails, trip_name, day, updated_by_name):
    subject = "One of your trips has been updated"
    body = f'{format_date(day)} of your trip "{trip_name}" was updated by {updated_by_name} on Collaborative Trip Planner.'
    sender_email = "collaborativetripplanner@gmail.com"
    sender_password = "fhqj mkxb imis qfnq"  
    smtp_server = "smtp.gmail.com"
    smtp_port = 587 

    print(f"Email body: {body}")

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ', '.join(emails) 
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  
            server.login(sender_email, sender_password) 
            text = msg.as_string()  
            server.sendmail(sender_email, emails, text)

        print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {str(e)}")

    
def email_trip_members(s):
    print("Emailing trip members...")
    parts = s.split('-')
    updated_by_user_id, trip_id, day = [parts[0], parts[1], '-'.join(parts[2:])]
    print(updated_by_user_id, trip_id, day)

    # retrieve emails of trip members, name of trip, and username of user who updated.
    trip_emails = get_trip_members_emails(trip_id)
    print(trip_emails)

    trip_name = get_trip_name(trip_id)
    print(trip_name)

    updated_by_name = get_user_who_updated(updated_by_user_id)
    print(updated_by_name)

    # send email alert to trip members about update
    send_email(trip_emails, trip_name, day, updated_by_name)



def retrieve_work_from_queue():
    while True:
        item = r.brpop(redis_queue, timeout=0)
        if item:
            _, updated_trip_str = item
            print(f"Trip updated. Retrieving {updated_trip_str.decode('utf-8')} from Redis queue...")
            email_trip_members(updated_trip_str.decode('utf-8'))




if __name__ == '__main__':
    retrieve_work_from_queue()