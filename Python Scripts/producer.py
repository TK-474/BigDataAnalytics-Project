import csv
import time
from confluent_kafka import Producer

print('start')

# Kafka Configuration
KAFKA_BROKER = 'localhost:9092'  # Update with your Kafka broker address
KAFKA_TOPIC = 'data4'  # Replace with your Kafka topic

# Initialize Kafka Producer
producer = Producer({'bootstrap.servers': KAFKA_BROKER})

# Callback for delivery confirmation
def delivery_report(err, msg):
    if err:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# File Configuration
CSV_FILE = 'data2.csv'  # Path to your CSV file
TIME_INTERVAL = 10  # Interval in seconds between each row (simulating real-time)
MAX_ROWS = 1000  # Limit to only 1000 rows

# Initialize row counter
row_count = 0

# Read CSV and send data to Kafka
try:
    with open(CSV_FILE, mode='r') as file:
        csv_reader = csv.DictReader(file)  # Use DictReader to handle headers
        for row in csv_reader:
            if row_count >= MAX_ROWS:
                break  # Stop after sending 1000 rows

            # Convert row to a string (or JSON if preferred)
            message = str(row)

            # Send message to Kafka
            producer.produce(
                topic=KAFKA_TOPIC,
                key=None,  # Optional: Use a key if needed
                value=message,
                callback=delivery_report
            )

            row_count += 1
            time.sleep(TIME_INTERVAL)  # Sleep for a certain time interval (optional)

            # Flush producer to ensure message delivery
            producer.flush()

except FileNotFoundError:
    print(f"Error: File '{CSV_FILE}' not found.")
except Exception as e:
    print(f"Error occurred: {e}")

print(f"Finished sending {row_count} rows to Kafka.")
