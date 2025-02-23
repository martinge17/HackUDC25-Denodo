#!/bin/bash

# Enable debug
set -x

# Set environment variable for Docker ports
DOCKER_PORTS=${BACKEND_PORT:-8888:80}

echo "-> Step 1: Building Docker image....."
# Build latest app docker image
docker build . --file Dockerfile --tag localhost/denodo-chat-backend-latest

echo "-> Step 1 Completed: Docker image built successfully!"

echo "-> Step 2: Stopping and removing old docker containers..."

# Stop and remove current docker container (if it does not exists, skip)
docker stop denodo-chat-back || true && docker rm denodo-chat-back || true

echo "-> Step 2 Done"

echo "-> Step 3: Running latest version...."
# Run latest version (previously created image)
docker run -d --name denodo-chat-back --env-file /home/hackudc25/.env -p $DOCKER_PORTS localhost/denodo-chat-backend-latest

echo "-> Step 3 Completed: Latest version deployed!"
