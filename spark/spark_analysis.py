from pyspark.sql import SparkSession
import os
from pyspark.sql.functions import col, regexp_replace, when, expr

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Transform and Combine Partitioned Files") \
    .getOrCreate()

# HDFS paths
input_directory = "hdfs://namenode:9000/data"
output_file = "hdfs://namenode:9000/transformation"

# List of file names (file1.csv, file2.csv, ..., fileN.csv)
num_files = 1  # Change this to the actual number of files
file_names = ['data.csv']

# Initialize an empty DataFrame

# final_df = None

# Iterate over each file and transform
for file_name in file_names:
    # Construct the full file path
    file_path = os.path.join(input_directory, file_name)
    
    # Load the file into a DataFrame
    df = spark.read.csv(file_path, header=True, inferSchema=True)
    
    # Remove commas and quotes from all string fields in the DataFrame
    for col_name in df.columns:
        df = df.withColumn(col_name, regexp_replace(col(col_name), r"[,'\"]", ""))

    # Transformation: Replace "Pakist" with "Pakistan" in the 'Country' column
    if 'Country' in df.columns:
        df = df.withColumn('Country', when(col('Country').like("%Pakist%"), "Pakistan").otherwise(col('Country')))

    # Transformation: Replace "GConsole" with "Gaming Console" in the 'ProductName' column
    if 'ProductName' in df.columns:
        df = df.withColumn('ProductName', when(col('ProductName').like("%GConsole%"), "Gaming Console").otherwise(col('ProductName')))

    # Transformation: Calculate TotalAmount as Price * Quantity
    if 'Price' in df.columns and 'Quantity' in df.columns:
        df = df.withColumn('TotalAmount', expr('Price * Quantity'))

    # Perform a transformation (example: replace nulls in 'Cabin' with "AAA")
    transformed_df = df

    # Append the transformed DataFrame to the final DataFrame
    # if final_df is None:
    #     final_df = transformed_df
    # else:
    #     final_df = final_df.union(transformed_df)

# Write the combined DataFrame to a single CSV file
# Reduce to a single partition for a single file output

transformed_df.coalesce(1).write.csv(output_file, header=False, mode="overwrite")

print("Transformation complete.")
