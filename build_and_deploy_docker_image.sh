#!/bin/bash
# Check if at least one argument is provided
if [ "$1" = "" ]; then
  echo "Usage: $0 <image tag> [environment]"
  exit 1
fi

environment=${2:-dev}

# exit when any command fails
set -e

docker build -t hkimhub/sbling-trip-api:"$1" .
docker stop sbling-trip-api || true
while [ ! -z "$(docker ps -q -f name=sbling-trip-api)" ]; do
    echo "Waiting for sbling-trip-api to stop..."
    sleep 1
done
docker run -d --rm \
  --name sbling-trip-api \
  --network my_custom_network \
  -p 8000:8000 \
  -e PHASE=$environment \
  hkimhub/sbling-trip-api:"$1"

#docker push hkimhub/sibling-trip-api:"$1"
