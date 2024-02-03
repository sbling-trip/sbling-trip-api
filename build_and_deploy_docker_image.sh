#!/bin/bash
if [ "$1" = "" ]
then
  echo "Usage: $0 <image tag>"
  exit 1
fi

# exit when any command fails
set -e

docker build -t hkimhub/sbling-trip-api:"$1" .
docker stop sbling-trip-api || true
docker run -d --rm \
  --name sbling-trip-api \
  --network my_custom_network \
  -p 8000:8000 \
  -e PHASE=prod \
  hkimhub/sbling-trip-api:"$1"

#docker push hkimhub/sibling-trip-api:"$1"
