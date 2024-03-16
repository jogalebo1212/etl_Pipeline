# Python 3.8 in docker images
FROM python:3.8

# Directory of work
WORKDIR /api

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy our source code
COPY ./app ./app

# Command by dafault when run main
CMD ["python", "./app/main.py"]