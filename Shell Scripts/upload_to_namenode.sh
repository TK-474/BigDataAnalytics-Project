#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# File to be copied
FILE="$SCRIPT_DIR/data1.csv"

# Check if the file exists
if [ ! -f "$FILE" ]; then
  echo "Error: data1.csv not found in the script directory!"
  exit 1
fi

# Check if the namenode container is running
if ! docker ps --format '{{.Names}}' | grep -q '^namenode$'; then
  echo "Error: namenode container is not running!"
  exit 1
fi

# Ensure the /data directory exists in the namenode container
docker exec namenode mkdir -p /data

# Copy the file to the namenode container with the new name
docker cp "$FILE" namenode:/data/temp_data1.csv
docker exec namenode mv /data/temp_data1.csv /data/data.csv

# Verify if the file was successfully copied and renamed
if docker exec namenode test -f /data/data.csv; then
  echo "File successfully copied and renamed to data.csv in /data inside namenode container."
else
  echo "Error: Failed to copy and rename the file to data.csv inside namenode container."
  exit 1
fi
