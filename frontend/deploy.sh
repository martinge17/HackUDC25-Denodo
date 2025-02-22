#!/bin/bash

# Enable debug
set -x

# Set environment variable for Docker ports
DOCKER_PORTS=${DENODO_PORT:-8080:8080}

echo "-> Step 1: Building Docker image....."
# Build latest app docker image
docker build . --file Dockerfile --tag localhost/denodo-chat-latest

echo "-> Step 1 Completed: Docker image built successfully!"

echo "-> Step 2: Stopping and removing old docker containers..."

# Stop and remove current docker container (if it does not exists, skip)
docker stop denodo-chat-front || true && docker rm denodo-chat-front || true

echo "-> Step 2 Done"

echo "-> Step 3: Running latest version...."
# Run latest version (previously created image)
docker run -d --name denodo-chat-front -p $DOCKER_PORTS localhost/denodo-chat-latest

echo "-> Step 3 Completed: Latest version deployed!"
