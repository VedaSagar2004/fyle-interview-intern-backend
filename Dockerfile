# Use Python 3.8 as the base image
FROM python:3.8

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Set environment variable for Flask application
ENV FLASK_APP=core/server.py

# Make port 5000 available to the world outside this container
EXPOSE 5000

# CMD is added in the docker-compose file