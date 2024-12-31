#!/bin/bash
FILE_NAME="data.csv"

# Create the target directory in HDFS if it doesn't already exist
docker exec -it namenode hdfs dfs -mkdir -p /data

# Remove the file in HDFS if it already exists
docker exec -it namenode hdfs dfs -rm -f /data/$FILE_NAME

# Upload the file to HDFS
docker exec -it namenode hdfs dfs -put /data/$FILE_NAME /data/

echo "File uploaded to HDFS: /data/$FILE_NAME"

