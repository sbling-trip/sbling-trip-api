#!/bin/bash
# Check if at least one argument is provided
if [ "$1" = "" ]; then
  echo "Usage: $0 <image tag> [environment]"
  exit 1
fi

# exit when any command fails
set -e

PASSWORD_FILE="/Users/kimhyun/.ssh/sbling-trip-docker-official"

# Read the password from the file
PASSWORD=$(cat "${PASSWORD_FILE}")

# Use the password for the docker login command
echo "${PASSWORD}" | docker login -u sblingtrip --password-stdin

docker build -t sblingtrip/sbling-trip-api:"$1" .
docker push sblingtrip/sbling-trip-api:"$1"
