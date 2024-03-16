# Python 3.8 in docker images
FROM python:3.8

# Directory of work
WORKDIR /ingest

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy our code for synchronizing the spin-up of interdependent services
COPY wait-for-it.sh /usr/wait-for-it.sh

# Copy our source code
COPY ./app ./app

# Run the wait-for-it
RUN chmod +x /usr/wait-for-it.sh