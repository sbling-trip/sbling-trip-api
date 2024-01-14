#!/bin/bash
if [ "$1" = "" ]
then
  echo "Usage: $0 <image tag>"
  exit 1
fi

# exit when any command fails
set -e

docker build -t hkimhub/sibling-trip-api:"$1" .
docker push hkimhub/sibling-trip-api:"$1"
