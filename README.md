# Big Data Processing and Dashboarding Project

## **Overview**
This project demonstrates a complete end-to-end pipeline for big data processing, transformation, and visualization. The aim is to simulate a real-world scenario for processing and analyzing large-scale e-commerce data using a modern big data stack. 

### **Key Technologies Used:**
- **Data Generation:** Python (Faker library)
- **Data Ingestion:** Kafka
- **Storage:** HDFS (Hadoop Distributed File System) and HBase
- **Data Processing:** Apache Spark
- **Visualization and Dashboarding:** Flask, Python, Pandas, Matplotlib/Plotly

---

## **Data Flow**

![Big Data Architecture](BDA_Project_Architecture.png)

### **1. Data Generation**
- **Why Generated Data?**
  - We were unable to find a suitable dataset of the required size on Kaggle.
  - A custom dataset was generated using Python's `Faker` library, ensuring the schema matched the project requirements.

- **Schema:**
  The data schema generated was as follows:
  ```
  - customer:CustomerID
  - customer:Name
  - customer:Age
  - customer:Country
  - customer:RegistrationDate
  - order:OrderDate
  - order:Quantity
  - order:TotalAmount
  - product:ProductID
  - product:ProductName
  - product:Category
  - product:Price
  - shipment:ShippingAddress
  - shipment:ShippingDate
  - row_key
  ```

- **Deliberate Data Errors:**
  - Missing values were introduced in some rows.
  - Errors such as typos and invalid values were deliberately included to simulate real-world messy data, allowing us to demonstrate data cleaning and transformation.

---

### **2. Data Storage**
#### **Initial Load to HDFS**
- An **800MB chunk of data** was loaded into HDFS manually via the NameNode.

#### **Streaming Remaining Data via Kafka**
- The rest of the data (approx. 1.2GB) was streamed incrementally via **Kafka** into the NameNode, which appended it to the already stored data in HDFS.
- **Kafka Topic:** `customer_orders`
- **Ingestion Workflow:**
  1. Python producer script streamed data row by row to Kafka.
  2. Spark Structured Streaming consumed Kafka data and appended it to HDFS.

---

### **3. Data Transformation**
#### **Apache Spark for Data Cleaning and Transformation**
- **Data Cleaning:**
  - Fixed missing values (e.g., filling null `Age` values with the median).
  - Corrected typos in country names and other string fields.

- **Data Transformation:**
  - Added derived columns such as `AgeGroup` (e.g., Young, Middle-aged, Senior).
  - Normalized numerical values like `TotalAmount` for downstream analytics.

- **Output:**
  - Transformed data was written back to HDFS in Parquet format for efficient storage and querying.

---

### **4. Storing Transformed Data in HBase**
- After transformation, the cleaned and processed data was loaded into **HBase**.
- **Schema in HBase:**
  - Table Name: `customer_orders`
  - Columns mapped to HBase column families and qualifiers.

#### **Workflow for HBase Loading:**
- Data was read from HDFS.
- Data was written to HBase using Spark’s HBase connector.

---

### **5. Data Access and Visualization**
#### **Accessing HBase Data via Thrift Server**
- Using HBase’s **Thrift Server**, we accessed the transformed data from HBase and loaded it into a Pandas DataFrame in Python.

#### **Exploratory Data Analysis (EDA)**
- Performed EDA to identify trends and patterns in the data, such as:
  - Customer demographics.
  - Most purchased products.
  - Monthly sales trends.

#### **Dashboard Creation**
- A Flask-based web application was created to display interactive dashboards.
- **Dashboards Included:**
  - Sales trends by category, region, and customer demographics.
  - Visualization of age distribution and total purchases.
  - Interactive filters for drilling down into the data.

---

## **Project Workflow**
### **1. Data Generation**
- Custom Python script generated e-commerce transactional data with realistic values and deliberate errors.

### **2. Data Ingestion**
- Data streamed to HDFS using Kafka and Spark.

### **3. Data Processing**
- Apache Spark cleaned and transformed the data.

### **4. Data Storage**
- Cleaned data was stored in HDFS and HBase for querying and visualization.

### **5. Dashboarding**
- Flask web application hosted dashboards for interactive data exploration.

---

## **Technologies Used**
| Component            | Technology        |
|----------------------|-------------------|
| Data Generation      | Python, Faker     |
| Data Ingestion       | Kafka             |
| Data Storage         | HDFS, HBase       |
| Data Processing      | Apache Spark      |
| Visualization        | Flask, Pandas, Plotly |

---

## **Challenges Faced**
1. **Handling Large Data Volumes:**
   - Chunking data ingestion via Kafka to avoid memory bottlenecks.

2. **Error Handling:**
   - Cleaning messy data required robust Spark transformations.

3. **Integration:**
   - Ensuring seamless data flow between Kafka, HDFS, Spark, and HBase.

---

## **Future Improvements**
1. Implement machine learning models for advanced analytics (e.g., customer segmentation).
2. Automate the entire pipeline using tools like Apache Airflow.
3. Scale the system for even larger datasets by leveraging a distributed Kafka setup.

---

## **How to Run the Project**
1. **Generate Data:**
   - Run the Python script to generate the dataset.
2. **Start Kafka:**
   - Set up Kafka and produce data to the `customer_orders` topic.
3. **Run Spark Jobs:**
   - Consume Kafka data, transform it, and store it in HDFS.
4. **Load Data to HBase:**
   - Use Spark to write transformed data into HBase.
5. **Launch Flask App:**
   - Start the Flask server and access dashboards at `http://localhost:5000`.

---

## **Conclusion**
This project demonstrates a robust big data processing pipeline, showcasing data generation, ingestion, transformation, storage, and visualization. It serves as a practical example of implementing big data technologies for scalable analytics.
