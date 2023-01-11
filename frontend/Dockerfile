# syntax=docker/dockerfile:1

# Base image
FROM node:18.12.1-bullseye-slim

# setup work environment variables
ENV NODE_ENV=production

# Create working directory
RUN mkdir -p /var/gumgumlearn/frontend

# Set working directory
WORKDIR /var/gumgumlearn/frontend

# Copy package json files
COPY ["package.json", "package-lock.json*", "./"]

# Refresh package index
RUN apt-get -y update

# Install security updates
RUN apt-get -y upgrade

# Install new linux packages
RUN apt-get -y install --no-install-recommends net-tools procps curl  iputils-ping apt-utils

# Delete cached files
RUN apt-get clean
RUN apt-get autoremove

# Delete package index files we dont need anymore
RUN rm -rf /var/lib/apt/lists/*

# install npm packages
RUN npm update -g npm
RUN npm install

# Copy our files
COPY . .

# Expose port to access vite server
EXPOSE 3000

# Create our docker ignore file
RUN echo "node_modules" > .dockerignore

# Start out vite server
ENTRYPOINT ["npm", "run", "start"]
