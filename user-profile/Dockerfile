# Dockerfile for frontend Flask app
FROM python:3.9-slim

# set working directory
WORKDIR /app

# Copy the requirements.txt and credential files into the container
COPY requirements.txt /app/
COPY db-serv-acc.json /app/db-serv-acc.json

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt --verbose

RUN pip3 install "cloud-sql-python-connector[pg8000]" --verbose

# Copy the rest of the application code into the container
COPY . /app/

# expose port for app to run on
EXPOSE 4000

# set environment variables
ENV DB_HOST=trip-planner-442220:us-central1:trip-planner-db
ENV DB_USER=postgres
ENV DB_NAME=postgres

CMD [ "python3", "user-rest-server.py" ]