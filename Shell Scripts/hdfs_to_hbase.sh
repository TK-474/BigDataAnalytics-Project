# #!/bin/bash

HBASE_CONTAINER_NAME="hbase"
NAMENODE_CONTAINER_NAME="namenode"
HBASE_COMMAND="hbase org.apache.hadoop.hbase.mapreduce.ImportTsv"
HDFS_DIRECTORY="/transformation"
HBASE_TABLE="ec"
# COLUMN_MAPPINGS="HBASE_ROW_KEY,cf:CustomerID,cf:CustomerName,cf:CustomerEmail,cf:CustomerAddress,cf:ProductID,cf:ProductName,cf:ProductCategory,cf:ProductPrice,cf:Quantity,cf:TotalPrice,cf:OrderDate"
COLUMN_MAPPINGS="HBASE_ROW_KEY,customer:CustomerID,product:ProductID,order:Quantity,order:OrderDate,shipment:ShippingAddress,shipment:ShippingDate,customer:Name,customer:Age,customer:Country,customer:RegistrationDate,product:ProductName,product:Category,product:Price,order:TotalAmount"
NEW_FILENAME="t_file.csv"


# Find the CSV file in the HDFS directory
CSV_FILE=""
FILES=$(docker exec $NAMENODE_CONTAINER_NAME hdfs dfs -ls hdfs://namenode:9000$HDFS_DIRECTORY)

while read -r line; do
    # Extract the last word (file path) from each line
    file_path=$(echo $line | rev | cut -d' ' -f1 | rev)
    
    # Check if the file path ends with .csv
    if [[ $file_path == *.csv ]]; then
        CSV_FILE=$file_path
        break
    fi
done <<< "$FILES"

# Check if a CSV file was found
if [ -z "$CSV_FILE" ]; then
    echo "No CSV file found in $HDFS_DIRECTORY."
    exit 1
fi

# Debug: Print the found CSV file
echo "Found CSV file: $CSV_FILE"

# Rename the found CSV file to the new name
docker exec $NAMENODE_CONTAINER_NAME hdfs dfs -mv "$CSV_FILE" "hdfs://namenode:9000$HDFS_DIRECTORY/$NEW_FILENAME"

# Debug: Print confirmation of renaming
if [ $? -eq 0 ]; then
    echo "Renamed $CSV_FILE to $HDFS_DIRECTORY/$NEW_FILENAME"
else
    echo "Failed to rename $CSV_FILE to $HDFS_DIRECTORY/$NEW_FILENAME"
fi

# Display the contents of the renamed file
docker exec -it $HBASE_CONTAINER_NAME bash -c "hbase org.apache.hadoop.hbase.mapreduce.ImportTsv -Dimporttsv.separator=, -Dimporttsv.columns='$COLUMN_MAPPINGS' ec hdfs://namenode:9000/transformation/t_file.csv"
