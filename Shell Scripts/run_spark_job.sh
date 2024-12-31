#!/bin/bash

docker exec -it namenode /bin/bash -c "hdfs dfs -rm -r /transformation"
SPARK_SCRIPT_PATH="/spark/spark_analysis.py"

# Copy Spark script to Spark Master container
docker cp ../spark/spark_analysis.py spark-master-bda:"$SPARK_SCRIPT_PATH"

# Run Spark job
docker exec -it spark-master-bda /bin/bash -c "/spark/bin/spark-submit $SPARK_SCRIPT_PATH"

echo "Spark job executed successfully."
