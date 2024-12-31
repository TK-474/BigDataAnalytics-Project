from faker import Faker
import pandas as pd
import numpy as np

# Initialize Faker
fake = Faker()

# Constants for data generation
ROW_COUNT = 6_000_000  # Maximum rows to generate
CHUNK_SIZE = 1000  # Number of rows per chunk for tracking
OUTPUT_FILE = "sample_customers.csv"

# Step 1: Predefine Customers
CUSTOMER_COUNT = 100_000  # Number of unique customers
customers = pd.DataFrame({
    "CustomerID": range(1, CUSTOMER_COUNT + 1),
    "Name": [fake.name() for _ in range(CUSTOMER_COUNT)],
    "Age": np.random.randint(18, 81, size=CUSTOMER_COUNT),
    "Country": np.random.choice(
        ["USA", "India", "Pakistan", "UK", "Canada", "Australia", "Germany", "France"],
        size=CUSTOMER_COUNT,
        replace=True
    ),
    "RegistrationDate": pd.to_datetime(
        np.random.randint(
            pd.Timestamp("2014-01-01").to_julian_date(),
            pd.Timestamp("2024-01-01").to_julian_date(),
            size=CUSTOMER_COUNT
        ),
        origin="julian",
        unit="D"
    )
})

# Step 2: Predefine Products
PRODUCT_COUNT = 20  # Number of unique products
products = pd.DataFrame({
    "ProductID": range(1, PRODUCT_COUNT + 1),
    "ProductName": [
        fake.word(ext_word_list=["Laptop", "Smartphone", "Headphones", "T-Shirt", "Microwave", "Tablet", "Novel", "Toy Car", "Blender", "Desk Lamp", "Shoes", "Backpack", "Washing Machine", "Smartwatch", "Camera", "Gaming Console", "Monitor", "Keyboard", "Mouse", "Printer"])
        for _ in range(PRODUCT_COUNT)
    ],
    "Category": [
        "Electronics" if name in ["Laptop", "Smartphone", "Headphones", "Tablet", "Smartwatch", "Camera", "Gaming Console", "Monitor", "Keyboard", "Mouse", "Printer"] else
        "Clothing" if name in ["T-Shirt", "Shoes", "Backpack"] else
        "Books" if name in ["Novel"] else
        "Home Appliances" if name in ["Microwave", "Blender", "Washing Machine", "Desk Lamp"] else
        "Toys"
        for name in ["Laptop", "Smartphone", "Headphones", "T-Shirt", "Microwave", "Tablet", "Novel", "Toy Car", "Blender", "Desk Lamp", "Shoes", "Backpack", "Washing Machine", "Smartwatch", "Camera", "Gaming Console", "Monitor", "Keyboard", "Mouse", "Printer"]
    ],
    "Price": np.round(np.random.uniform(10, 1000, size=PRODUCT_COUNT), 2)
})

# Step 3: Generate Data in Chunks
def generate_and_save_data():
    with open(OUTPUT_FILE, mode="w", encoding="utf-8", newline="") as f:
        header_written = False  # Flag to track if header is written

        for i in range(0, ROW_COUNT, CHUNK_SIZE):
            customer_ids = np.random.choice(customers["CustomerID"], size=CHUNK_SIZE, replace=True)
            product_ids = np.random.choice(products["ProductID"], size=CHUNK_SIZE, replace=True)

            chunk = pd.DataFrame({
                "OrderID": range(i + 1, i + CHUNK_SIZE + 1),
                "CustomerID": customer_ids,
                "ProductID": product_ids,
                "Quantity": np.random.randint(1, 10, size=CHUNK_SIZE),
                "OrderDate": pd.to_datetime(
                    np.random.randint(
                        pd.Timestamp("2020-01-01").to_julian_date(),
                        pd.Timestamp("2024-01-01").to_julian_date(),
                        size=CHUNK_SIZE
                    ),
                    origin="julian",
                    unit="D"
                ),
                "ShippingAddress": [fake.address().replace("\n", " ") for _ in range(CHUNK_SIZE)],
                "ShippingDate": pd.to_datetime(
                    np.random.randint(
                        pd.Timestamp("2020-01-02").to_julian_date(),
                        pd.Timestamp("2024-01-05").to_julian_date(),
                        size=CHUNK_SIZE
                    ),
                    origin="julian",
                    unit="D"
                )
            })

            chunk = chunk.merge(customers, on="CustomerID", how="left")
            chunk = chunk.merge(products, on="ProductID", how="left")
            chunk["TotalAmount"] = np.round(chunk["Price"] * chunk["Quantity"], 2)

            # Save to CSV incrementally
            chunk.to_csv(f, mode="a", index=False, header=not header_written)
            header_written = True

            # Print progress
            print(f"Generated and saved {i + CHUNK_SIZE} rows so far...")

# Run the data generation
generate_and_save_data()

print(f"Generated {ROW_COUNT} rows of data and saved to {OUTPUT_FILE}")
