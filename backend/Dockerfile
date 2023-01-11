# syntax=docker/dockerfile:1

# Base image
FROM python:3.8.16-slim-bullseye

# Create our folders
RUN mkdir -p /var/motobay/backend

ENV PYTHONIOENCODING="UTF-8"
ENV PYTHONPATH="./"
ENV GUMGUMLEARN_API_HOST="gumgumlearn_api_host"
ENV GUMGUMLEARN_API_PORT="8000"
ENV GUMGUMLEARN_ENV="prod"
ENV GUMGUMLEARN_POSTGRESQL_USER="learn_test"
ENV GUMGUMLEARN_POSTGRESQL_PWD="learn_test_pwd"
ENV GUMGUMLEARN_POSTGRESQL_HOST="gumgumlearn_db_host"
ENV GUMGUMLEARN_POSTGRESQL_DB="learn_test_db"

# Set working directory
WORKDIR /var/gumgumlearn/backend

# Copy requirements.txt file
COPY requirements.txt requirements.txt

# Refresh package index
RUN apt-get -y update

# Install security updates
RUN apt-get -y upgrade

# Install new linux packages
RUN apt-get -y install --no-install-recommends procps apt-utils net-tools curl pkg-config iputils-ping

# Delete cached files
RUN apt-get clean
RUN apt-get autoremove

# Delete package index files we dont need anymore
RUN rm -rf /var/lib/apt/lists/*

# Install python package dependencies for the project
RUN pip3 install pip --upgrade
RUN pip3 install --no-cache-dir -U -r requirements.txt

# Copy our files
COPY . .

# Expose port to access uvicorn server
EXPOSE 8000

# Start our server
ENTRYPOINT ["python3", "main.py"]
