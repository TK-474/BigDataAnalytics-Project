import os
import csv
import subprocess
from confluent_kafka import Consumer, KafkaException

print("Consumer started")

# Kafka Configuration
KAFKA_BROKER = 'localhost:9092'  # Update with your Kafka broker address
KAFKA_TOPIC = 'data4'  # Replace with your Kafka topic
GROUP_ID = 'ecommerce-consumer-group'  # Consumer group ID

# Initialize Kafka Consumer
consumer = Consumer({
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': GROUP_ID,
    'auto.offset.reset': 'earliest',
    'fetch.min.bytes': 1048576  # Fetch at least 1 MB of data
})

# Subscribe to the Kafka topic
consumer.subscribe([KAFKA_TOPIC])

# File Configuration
LOCAL_FILE = '/data/data.csv'  # CSV file path inside the container
CONTAINER_NAME = "namenode"  # Replace with your container ID

# Function to check if the file exists in the container and create it if it doesn't
def create_file_if_not_exists(container_name, file_path):
    """Checks if the file exists in the container. If not, creates it."""
    try:
        # Command to check if the file exists, if not create it (without writing a header)
        check_command = f"if [ ! -f {file_path} ]; then touch {file_path}; fi"
        subprocess.run(
            ["docker", "exec", container_name, "bash", "-c", check_command],
            check=True
        )
    except Exception as e:
        print(f"Failed to check or create file in container: {e}")

# Function to append data as CSV rows in the container
def append_to_csv_in_container(container_name, file_path, row_data=None):
    """
    Appends a row of data to a CSV file in the container.
    """
    try:
        # If the file doesn't exist, create it
        create_file_if_not_exists(container_name, file_path)
        
        # Command to append the row data to the file
        if row_data:
            row_command = f"echo '{','.join(row_data)}' >> {file_path}"
            subprocess.run(
                ["docker", "exec", container_name, "bash", "-c", row_command],
                check=True
            )

    except Exception as e:
        print(f"Failed to write to CSV file inside container: {e}")

try:
    print(f"Listening to topic: {KAFKA_TOPIC}")
    while True:
        # Poll for messages with a timeout
        msg = consumer.poll(timeout=1.0)

        if msg is None:  # No message
            continue
        if msg.error():  # Error occurred
            if msg.error().code() == KafkaException._PARTITION_EOF:
                continue  # End of partition
            else:
                print(f"Error: {msg.error()}")
                break

        # Message received
        message = msg.value().decode('utf-8')
        print(f"Received message: {message}")

        # Parse the message into CSV format (convert string to dictionary)
        row_data = eval(message)  # Convert string back to dictionary
        row_data['ShippingAddress'] = f'"{row_data["ShippingAddress"]}"'

        append_to_csv_in_container(CONTAINER_NAME, LOCAL_FILE, row_data=list(row_data.values()))

except KeyboardInterrupt:
    print("Consumer stopped manually.")
except Exception as e:
    print(f"Error occurred: {e}")
finally:
    # Close the consumer
    consumer.close()
    print("Consumer closed.")
