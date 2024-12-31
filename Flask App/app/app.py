# # from flask import Flask

# # app = Flask(__name__)

# # @app.route('/')
# # def hello():
# #     return "Heyywfefey!"

# # if __name__ == '__main__':
# #     app.run(host='0.0.0.0', port=8000, debug=True)


# from flask import Flask, render_template_string, Response
# import happybase
# import pandas as pd
# import matplotlib.pyplot as plt
# import io

# app = Flask(__name__)

# @app.route('/')
# def hello():
#     return "Heyyy!"

# @app.route('/hbase-stats')
# def hbase_stats():
#     try:
#         # Connect to HBase Thrift Server
#         connection = happybase.Connection(host='172.19.0.8', port=9090)  # Replace with your container IP
#         table = connection.table('Orders')

#         # Fetch data
#         rows = table.scan()
#         data = []
#         for key, row in rows:
#             row_data = {
#                 (k.decode('utf-8').split(':')[1] if k.decode('utf-8').startswith('cf:') else k.decode('utf-8')): v.decode('utf-8')
#                 for k, v in row.items()
#             }  # Decode binary data and strip 'cf:' prefix
#             row_data['OrderID'] = key.decode('utf-8')  # Use row key as 'OrderID'
#             data.append(row_data)

#         # Convert to pandas DataFrame
#         df = pd.DataFrame(data)

#         # Convert numeric columns to appropriate types
#         numeric_columns = ['ProductPrice', 'Quantity', 'TotalPrice']
#         df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)
#         df['OrderDate'] = pd.to_datetime(df['OrderDate'])

#         # Analysis and Statistics
#         stats_summary = df.describe(include='all').transpose()  # Transpose for better readability

#         # Additional Insights
#         total_revenue = df['TotalPrice'].sum()
#         most_popular_product = df['ProductName'].value_counts().idxmax()
#         most_popular_category = df['ProductCategory'].value_counts().idxmax()
#         top_customer = df['CustomerName'].value_counts().idxmax()
#         total_orders = df['OrderID'].nunique()

#         # Render Analysis in HTML
#         stats_html = stats_summary.to_html(classes='table table-striped')

#         html_template = f"""
#         <!doctype html>
#         <html>
#         <head>
#             <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css">
#             <title>HBase Table Statistics</title>
#         </head>
#         <body>
#             <div class="container mt-4">
#                 <h1>HBase Table Statistics</h1>
#                 <h3>Summary Statistics</h3>
#                 {stats_html}
#                 <h3>Additional Insights</h3>
#                 <ul>
#                     <li>Total Revenue: <strong>${total_revenue:.2f}</strong></li>
#                     <li>Most Popular Product: <strong>{most_popular_product}</strong></li>
#                     <li>Most Popular Category: <strong>{most_popular_category}</strong></li>
#                     <li>Top Customer: <strong>{top_customer}</strong></li>
#                     <li>Total Orders: <strong>{total_orders}</strong></li>
#                 </ul>
#             </div>
#         </body>
#         </html>
#         """
#         return html_template

#     except Exception as e:
#         return f"Error: {str(e)}"
    
# @app.route('/hbase-charts')
# def hbase_charts():
#     try:
#         # Connect to HBase Thrift Server
#         connection = happybase.Connection(host='172.19.0.8', port=9090)
#         table = connection.table('Orders')

#         # Fetch data
#         rows = table.scan()
#         data = []
#         for key, row in rows:
#             row_data = {
#                 (k.decode('utf-8').split(':')[1] if k.decode('utf-8').startswith('cf:') else k.decode('utf-8')): v.decode('utf-8')
#                 for k, v in row.items()
#             }
#             row_data['OrderID'] = key.decode('utf-8')
#             data.append(row_data)

#         # Convert to pandas DataFrame
#         df = pd.DataFrame(data)

#         # Convert numeric columns to appropriate types
#         numeric_columns = ['ProductPrice', 'Quantity', 'TotalPrice']
#         df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)
#         df['OrderDate'] = pd.to_datetime(df['OrderDate'])

#         # Generate a bar chart
#         plt.figure(figsize=(8, 6))
#         df.groupby('ProductCategory')['TotalPrice'].sum().plot(kind='bar')
#         plt.title('Total Revenue by Product Category')
#         plt.ylabel('Total Revenue')
#         plt.xlabel('Product Category')
#         plt.tight_layout()

#         # Save plot to an in-memory file
#         img = io.BytesIO()
#         plt.savefig(img, format='png')
#         img.seek(0)
#         plt.close()

#         # Return the image as a response
#         return Response(img, mimetype='image/png')

#     except Exception as e:
#         return f"Error: {str(e)}"
    

# @app.route('/hbase-datewise-sales')
# def hbase_datewise_sales():
#     try:
#         # Connect to HBase Thrift Server
#         connection = happybase.Connection(host='172.19.0.8', port=9090)
#         table = connection.table('Orders')

#         # Fetch data
#         rows = table.scan()
#         data = []
#         for key, row in rows:
#             row_data = {
#                 (k.decode('utf-8').split(':')[1] if k.decode('utf-8').startswith('cf:') else k.decode('utf-8')): v.decode('utf-8')
#                 for k, v in row.items()
#             }
#             row_data['OrderID'] = key.decode('utf-8')
#             data.append(row_data)

#         # Convert to pandas DataFrame
#         df = pd.DataFrame(data)

#         # Convert numeric columns to appropriate types
#         numeric_columns = ['ProductPrice', 'Quantity', 'TotalPrice']
#         df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)
#         df['OrderDate'] = pd.to_datetime(df['OrderDate'])

#         # Generate a line chart for datewise sales
#         plt.figure(figsize=(10, 6))
#         df.groupby('OrderDate')['TotalPrice'].sum().plot(kind='line', marker='o')
#         plt.title('Datewise Sales')
#         plt.ylabel('Total Revenue')
#         plt.xlabel('Order Date')
#         plt.grid(True)
#         plt.tight_layout()

#         # Save plot to an in-memory file
#         img = io.BytesIO()
#         plt.savefig(img, format='png')
#         img.seek(0)
#         plt.close()

#         # Return the image as a response
#         return Response(img, mimetype='image/png')

#     except Exception as e:
#         return f"Error: {str(e)}"

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=True)

#CORRECT

# from flask import Flask, jsonify, Response, render_template_string
# import happybase
# import pandas as pd
# import matplotlib.pyplot as plt
# import io

# app = Flask(__name__)

# # Global variable to store the DataFrame
# dataframe = None

# # Connect to HBase
# HBASE_HOST = '172.18.0.8'  # Replace with your HBase host
# HBASE_PORT = 9090         # Replace with your HBase Thrift port
# TABLE_NAME = 'ec'


# # Function to typecast the DataFrame
# def typecast_dataframe(df):
#     try:
#         # Define typecasting for each column
#         df['customer:Age'] = pd.to_numeric(df['customer:Age'], errors='coerce')  # Convert to numeric (integer)
#         df['customer:Country'] = df['customer:Country'].astype(str)  # Ensure string type
#         df['customer:CustomerID'] = pd.to_numeric(df['customer:CustomerID'], errors='coerce')  # Convert to integer
#         df['customer:Name'] = df['customer:Name'].astype(str)  # Ensure string type
#         df['customer:RegistrationDate'] = pd.to_datetime(df['customer:RegistrationDate'], errors='coerce')  # Convert to datetime
#         df['order:OrderDate'] = pd.to_datetime(df['order:OrderDate'], errors='coerce')  # Convert to datetime
#         df['order:Quantity'] = pd.to_numeric(df['order:Quantity'], errors='coerce')  # Convert to numeric
#         df['order:TotalAmount'] = pd.to_numeric(df['order:TotalAmount'], errors='coerce')  # Convert to float
#         df['product:Category'] = df['product:Category'].astype(str)  # Ensure string type
#         df['product:Price'] = pd.to_numeric(df['product:Price'], errors='coerce')  # Convert to float
#         df['product:ProductID'] = pd.to_numeric(df['product:ProductID'], errors='coerce')  # Convert to integer
#         df['product:ProductName'] = df['product:ProductName'].astype(str)  # Ensure string type
#         df['shipment:ShippingAddress'] = df['shipment:ShippingAddress'].astype(str)  # Ensure string type
#         df['shipment:ShippingDate'] = pd.to_datetime(df['shipment:ShippingDate'], errors='coerce')  # Convert to datetime
#         df['row_key'] = df['row_key'].astype(str)  # Ensure string type
#         return df
#     except Exception as e:
#         raise ValueError(f"Error in typecasting: {e}")

# # Endpoint to load the DataFrame from HBase
# @app.route('/', methods=['GET'])
# def load_data():
#     global dataframe
#     try:
#         # Connect to HBase Thrift Server
#         connection = happybase.Connection(host=HBASE_HOST, port=HBASE_PORT)
#         table = connection.table(TABLE_NAME)

#         # Fetch data using table.scan()
#         rows = table.scan(batch_size=1000)  # Adjust batch size if needed
#         data = [
#             {**{k.decode('utf-8'): v.decode('utf-8') for k, v in row.items()}, 'row_key': key.decode('utf-8')}
#             for key, row in rows
#         ]

#         # Convert to pandas DataFrame
#         dataframe = pd.DataFrame(data)

#         # Typecast the DataFrame
#         dataframe = typecast_dataframe(dataframe)

#         return jsonify({"message": "DataFrame loaded and typecasted successfully!", "rows": len(dataframe)})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Endpoint to get statistics by category
# @app.route('/customer', methods=['GET'])
# def category_stats():
#     global dataframe
#     if dataframe is None:
#         return jsonify({"error": "DataFrame not loaded. Please visit /load first."}), 400

#     try:
#     # Find top 5 customers by total amount spent. Get customer name, age, country, and total amount spent.
#         top_customers = dataframe.groupby('customer:CustomerID').agg(
#             CustomerName=('customer:Name', 'first'),
#             Age=('customer:Age', 'first'),
#             Country=('customer:Country', 'first'),
#             TotalAmount=('order:TotalAmount', 'sum')
#         ).sort_values(by='TotalAmount', ascending=False).head(5)

#         # Put this in a HTML table
#         top_customers_html = top_customers.to_html(classes='table table-striped')

#         return top_customers_html
#     except Exception as e:
#         return f"Error: {str(e)}"

# # Endpoint to get statistics by Product
# @app.route('/product', methods=['GET'])
# def product_stats():
#     global dataframe
#     if dataframe is None:
#         return jsonify({"error": "DataFrame not loaded. Please visit /load first."}), 400

#     try:
#     # Find top 5 products by total amount sold. Get product name, category, price, and total amount sold.
#         top_products = dataframe.groupby('product:ProductID').agg(
#             ProductName=('product:ProductName', 'first'),
#             Category=('product:Category', 'first'),
#             Price=('product:Price', 'first'),
#             TotalAmount=('order:TotalAmount', 'sum')
#         ).sort_values(by='TotalAmount', ascending=False).head(5)

#         # Put this in a HTML table
#         top_products_html = top_products.to_html(classes='table table-striped')

#         return top_products_html
#     except Exception as e:
#         return f"Error: {str(e)}"
    
# # Endpoint to get plot sales by date
# @app.route('/sales', methods=['GET'])
# def sales_plot():
#     global dataframe
#     if dataframe is None:
#         return jsonify({"error": "DataFrame not loaded. Please visit /load first."}), 400

#     try:
#         # Generate a line chart for datewise sales
#         plt.figure(figsize=(10, 6))
#         dataframe.groupby('order:OrderDate')['order:TotalAmount'].sum().plot(kind='line', marker='o')
#         plt.title('Datewise Sales')
#         plt.ylabel('Total Revenue')
#         plt.xlabel('Order Date')
#         plt.grid(True)
#         plt.tight_layout()

#         # Save plot to an in-memory file
#         img = io.BytesIO()
#         plt.savefig(img, format='png')
#         img.seek(0)
#         plt.close()

#         # Return the image as a response
#         return Response(img, mimetype='image/png')

#     except Exception as e:
#         return f"Error: {str(e)}"

# # Endpoint to find most loyal customers
# @app.route('/loyal', methods=['GET'])
# def loyal_customers():
#     global dataframe
#     if dataframe is None:
#         return jsonify({"error": "DataFrame not loaded. Please visit /load first."}), 400

#     try:
#         # Find top 5 loyal customers by number of orders. Get customer name, age, country, and number of orders.
#         loyal_customers = dataframe.groupby('customer:CustomerID').agg(
#             CustomerName=('customer:Name', 'first'),
#             Age=('customer:Age', 'first'),
#             Country=('customer:Country', 'first'),
#             Orders=('order:OrderDate', 'count')
#         ).sort_values(by='Orders', ascending=False).head(5)

#         # Put this in a HTML table
#         loyal_customers_html = loyal_customers.to_html(classes='table table-striped')

#         return loyal_customers_html
#     except Exception as e:
#         return f"Error: {str(e)}"
    

# # Endpoint to find counrties with lowest sales
# @app.route('/low', methods=['GET'])
# def low_sales():
#     global dataframe
#     if dataframe is None:
#         return jsonify({"error": "DataFrame not loaded. Please visit /load first."}), 400

#     try:
#         # Find top 5 countries with lowest sales. Get country name and total amount sold.
#         low_sales = dataframe.groupby('customer:Country').agg(
#             TotalAmount=('order:TotalAmount', 'sum')
#         ).sort_values(by='TotalAmount', ascending=True).head(5)

#         # Put this in a HTML table
#         low_sales_html = low_sales.to_html(classes='table table-striped')

#         return low_sales_html
#     except Exception as e:
#         return f"Error: {str(e)}"
    
# # Pie chart for sales by category and another for sales by country
# @app.route('/pie', methods=['GET'])
# def pie_chart():
#     global dataframe
#     if dataframe is None:
#         return jsonify({"error": "DataFrame not loaded. Please visit /load first."}), 400

#     try:
#         # Generate a pie chart for sales by category
#         img_category = io.BytesIO()
#         plt.figure(figsize=(10, 6))
#         dataframe.groupby('product:Category')['order:TotalAmount'].sum().plot(kind='pie', autopct='%1.1f%%')
#         plt.title('Sales by Category')
#         plt.ylabel('')
#         plt.tight_layout()
#         plt.savefig(img_category, format='png')
#         img_category.seek(0)
#         plt.close()

#         # Generate a pie chart for sales by country
#         img_country = io.BytesIO()
#         plt.figure(figsize=(10, 6))
#         dataframe.groupby('customer:Country')['order:TotalAmount'].sum().plot(kind='pie', autopct='%1.1f%%')
#         plt.title('Sales by Country')
#         plt.ylabel('')
#         plt.tight_layout()
#         plt.savefig(img_country, format='png')
#         img_country.seek(0)
#         plt.close()

#         # Embed images in HTML
#         html_template = """
#         <html>
#         <head><title>Pie Charts</title></head>
#         <body>
#             <h1>Sales by Category</h1>
#             <img src="data:image/png;base64,{{ category_chart }}" alt="Sales by Category">
#             <h1>Sales by Country</h1>
#             <img src="data:image/png;base64,{{ country_chart }}" alt="Sales by Country">
#         </body>
#         </html>
#         """

#         # Encode images to base64
#         import base64
#         category_chart = base64.b64encode(img_category.getvalue()).decode('utf-8')
#         country_chart = base64.b64encode(img_country.getvalue()).decode('utf-8')

#         # Render HTML with embedded images
#         return render_template_string(html_template, category_chart=category_chart, country_chart=country_chart)

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Run the Flask app
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=True)



# from flask import Flask, jsonify, Response, render_template_string
# import happybase
# import pandas as pd
# import matplotlib.pyplot as plt
# import io

# app = Flask(__name__)

# # Global variable to store the DataFrame
# dataframe = None

# # Connect to HBase
# HBASE_HOST = '172.18.0.8'  # Replace with your HBase host
# HBASE_PORT = 9090         # Replace with your HBase Thrift port
# TABLE_NAME = 'ec'

# # Function to typecast the DataFrame
# def typecast_dataframe(df):
#     try:
#         # Define typecasting for each column
#         df['customer:Age'] = pd.to_numeric(df['customer:Age'], errors='coerce')  # Convert to numeric (integer)
#         df['customer:Country'] = df['customer:Country'].astype(str)  # Ensure string type
#         df['customer:CustomerID'] = pd.to_numeric(df['customer:CustomerID'], errors='coerce')  # Convert to integer
#         df['customer:Name'] = df['customer:Name'].astype(str)  # Ensure string type
#         df['customer:RegistrationDate'] = pd.to_datetime(df['customer:RegistrationDate'], errors='coerce')  # Convert to datetime
#         df['order:OrderDate'] = pd.to_datetime(df['order:OrderDate'], errors='coerce')  # Convert to datetime
#         df['order:Quantity'] = pd.to_numeric(df['order:Quantity'], errors='coerce')  # Convert to numeric
#         df['order:TotalAmount'] = pd.to_numeric(df['order:TotalAmount'], errors='coerce')  # Convert to float
#         df['product:Category'] = df['product:Category'].astype(str)  # Ensure string type
#         df['product:Price'] = pd.to_numeric(df['product:Price'], errors='coerce')  # Convert to float
#         df['product:ProductID'] = pd.to_numeric(df['product:ProductID'], errors='coerce')  # Convert to integer
#         df['product:ProductName'] = df['product:ProductName'].astype(str)  # Ensure string type
#         df['shipment:ShippingAddress'] = df['shipment:ShippingAddress'].astype(str)  # Ensure string type
#         df['shipment:ShippingDate'] = pd.to_datetime(df['shipment:ShippingDate'], errors='coerce')  # Convert to datetime
#         df['row_key'] = df['row_key'].astype(str)  # Ensure string type
#         return df
#     except Exception as e:
#         raise ValueError(f"Error in typecasting: {e}")

# # Endpoint to load the DataFrame from HBase
# @app.route('/', methods=['GET'])
# def homepage():
#     html_template = """
#     <html>
#     <head><title>Data Analytics Dashboard</title></head>
#     <body>
#         <h1>Welcome to the Data Analytics Dashboard</h1>
#         <nav>
#             <ul>
#                 <li><a href="/load">Load Data</a></li>
#                 <li><a href="/customer">Top Customers</a></li>
#                 <li><a href="/product">Top Products</a></li>
#                 <li><a href="/sales">Sales by Date</a></li>
#                 <li><a href="/loyal">Loyal Customers</a></li>
#                 <li><a href="/low">Lowest Sales by Country</a></li>
#                 <li><a href="/pie">Sales Pie Charts</a></li>
#             </ul>
#         </nav>
#     </body>
#     </html>
#     """
#     return render_template_string(html_template)

# # Existing endpoints
# @app.route('/load', methods=['GET'])
# def load_data():
#     global dataframe
#     try:
#         # Connect to HBase Thrift Server
#         connection = happybase.Connection(host=HBASE_HOST, port=HBASE_PORT)
#         table = connection.table(TABLE_NAME)

#         # Fetch data using table.scan()
#         rows = table.scan(batch_size=1000)  # Adjust batch size if needed
#         data = [
#             {**{k.decode('utf-8'): v.decode('utf-8') for k, v in row.items()}, 'row_key': key.decode('utf-8')}
#             for key, row in rows
#         ]

#         # Convert to pandas DataFrame
#         dataframe = pd.DataFrame(data)

#         # Typecast the DataFrame
#         dataframe = typecast_dataframe(dataframe)

#         return jsonify({"message": "DataFrame loaded and typecasted successfully!", "rows": len(dataframe)})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/customer', methods=['GET'])
# def category_stats():
#     global dataframe
#     if dataframe is None:
#         return jsonify({"error": "DataFrame not loaded. Please visit /load first."}), 400

#     try:
#         # Find top 5 customers by total amount spent. Get customer name, age, country, and total amount spent.
#         top_customers = dataframe.groupby('customer:CustomerID').agg(
#             CustomerName=('customer:Name', 'first'),
#             Age=('customer:Age', 'first'),
#             Country=('customer:Country', 'first'),
#             TotalAmount=('order:TotalAmount', 'sum')
#         ).sort_values(by='TotalAmount', ascending=False).head(5)

#         # Put this in a HTML table
#         top_customers_html = top_customers.to_html(classes='table table-striped')

#         return top_customers_html
#     except Exception as e:
#         return f"Error: {str(e)}"

# @app.route('/product', methods=['GET'])
# def product_stats():
#     global dataframe
#     if dataframe is None:
#         return jsonify({"error": "DataFrame not loaded. Please visit /load first."}), 400

#     try:
#         # Find top 5 products by total amount sold. Get product name, category, price, and total amount sold.
#         top_products = dataframe.groupby('product:ProductID').agg(
#             ProductName=('product:ProductName', 'first'),
#             Category=('product:Category', 'first'),
#             Price=('product:Price', 'first'),
#             TotalAmount=('order:TotalAmount', 'sum')
#         ).sort_values(by='TotalAmount', ascending=False).head(5)

#         # Put this in a HTML table
#         top_products_html = top_products.to_html(classes='table table-striped')

#         return top_products_html
#     except Exception as e:
#         return f"Error: {str(e)}"

# @app.route('/sales', methods=['GET'])
# def sales_plot():
#     global dataframe
#     if dataframe is None:
#         return jsonify({"error": "DataFrame not loaded. Please visit /load first."}), 400

#     try:
#         # Generate a line chart for datewise sales
#         plt.figure(figsize=(10, 6))
#         dataframe.groupby('order:OrderDate')['order:TotalAmount'].sum().plot(kind='line', marker='o')
#         plt.title('Datewise Sales')
#         plt.ylabel('Total Revenue')
#         plt.xlabel('Order Date')
#         plt.grid(True)
#         plt.tight_layout()

#         # Save plot to an in-memory file
#         img = io.BytesIO()
#         plt.savefig(img, format='png')
#         img.seek(0)
#         plt.close()

#         # Return the image as a response
#         return Response(img, mimetype='image/png')

#     except Exception as e:
#         return f"Error: {str(e)}"

# @app.route('/loyal', methods=['GET'])
# def loyal_customers():
#     global dataframe
#     if dataframe is None:
#         return jsonify({"error": "DataFrame not loaded. Please visit /load first."}), 400

#     try:
#         # Find top 5 loyal customers by number of orders. Get customer name, age, country, and number of orders.
#         loyal_customers = dataframe.groupby('customer:CustomerID').agg(
#             CustomerName=('customer:Name', 'first'),
#             Age=('customer:Age', 'first'),
#             Country=('customer:Country', 'first'),
#             Orders=('order:OrderDate', 'count')
#         ).sort_values(by='Orders', ascending=False).head(5)

#         # Put this in a HTML table
#         loyal_customers_html = loyal_customers.to_html(classes='table table-striped')

#         return loyal_customers_html
#     except Exception as e:
#         return f"Error: {str(e)}"

# @app.route('/low', methods=['GET'])
# def low_sales():
#     global dataframe
#     if dataframe is None:
#         return jsonify({"error": "DataFrame not loaded. Please visit /load first."}), 400

#     try:
#         # Find top 5 countries with lowest sales. Get country name and total amount sold.
#         low_sales = dataframe.groupby('customer:Country').agg(
#             TotalAmount=('order:TotalAmount', 'sum')
#         ).sort_values(by='TotalAmount', ascending=True).head(5)

#         # Put this in a HTML table
#         low_sales_html = low_sales.to_html(classes='table table-striped')

#         return low_sales_html
#     except Exception as e:
#         return f"Error: {str(e)}"

# @app.route('/pie', methods=['GET'])
# def pie_chart():
#     global dataframe
#     if dataframe is None:
#         return jsonify({"error": "DataFrame not loaded. Please visit /load first."}), 400

#     try:
#         # Generate a pie chart for sales by category
#         img_category = io.BytesIO()
#         plt.figure(figsize=(10, 6))
#         dataframe.groupby('product:Category')['order:TotalAmount'].sum().plot(kind='pie', autopct='%1.1f%%')
#         plt.title('Sales by Category')
#         plt.ylabel('')
#         plt.tight_layout()
#         plt.savefig(img_category, format='png')
#         img_category.seek(0)
#         plt.close()

#         # Generate a pie chart for sales by country
#         img_country = io.BytesIO()
#         plt.figure(figsize=(10, 6))
#         dataframe.groupby('customer:Country')['order:TotalAmount'].sum().plot(kind='pie', autopct='%1.1f%%')
#         plt.title('Sales by Country')
#         plt.ylabel('')
#         plt.tight_layout()
#         plt.savefig(img_country, format='png')
#         img_country.seek(0)
#         plt.close()

#         # Embed images in HTML
#         html_template = """
#         <html>
#         <head><title>Pie Charts</title></head>
#         <body>
#             <h1>Sales by Category</h1>
#             <img src="data:image/png;base64,{{ category_chart }}" alt="Sales by Category">
#             <h1>Sales by Country</h1>
#             <img src="data:image/png;base64,{{ country_chart }}" alt="Sales by Country">
#         </body>
#         </html>
#         """

#         # Encode images to base64
#         import base64
#         category_chart = base64.b64encode(img_category.getvalue()).decode('utf-8')
#         country_chart = base64.b64encode(img_country.getvalue()).decode('utf-8')

#         # Render HTML with embedded images
#         return render_template_string(html_template, category_chart=category_chart, country_chart=country_chart)

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Run the Flask app
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=True)



from flask import Flask, jsonify, Response, render_template_string
import happybase
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from flask import request

app = Flask(__name__)

# Global variable to store the DataFrame
dataframe = None

# Connect to HBase
HBASE_HOST = '172.21.0.7'  # Replace with your HBase host
# HBASE_HOST = 'localhost'  # Replace with your HBase host
HBASE_PORT = 9090         # Replace with your HBase Thrift port
TABLE_NAME = 'ec'

# Function to typecast the DataFrame
def typecast_dataframe(df):
    try:
        # Define typecasting for each column
        df['customer:Age'] = pd.to_numeric(df['customer:Age'], errors='coerce')  # Convert to numeric (integer)
        df['customer:Country'] = df['customer:Country'].astype(str)  # Ensure string type
        df['customer:CustomerID'] = pd.to_numeric(df['customer:CustomerID'], errors='coerce')  # Convert to integer
        df['customer:Name'] = df['customer:Name'].astype(str)  # Ensure string type
        df['customer:RegistrationDate'] = pd.to_datetime(df['customer:RegistrationDate'], errors='coerce')  # Convert to datetime
        df['order:OrderDate'] = pd.to_datetime(df['order:OrderDate'], errors='coerce')  # Convert to datetime
        df['order:Quantity'] = pd.to_numeric(df['order:Quantity'], errors='coerce')  # Convert to numeric
        df['order:TotalAmount'] = pd.to_numeric(df['order:TotalAmount'], errors='coerce')  # Convert to float
        df['product:Category'] = df['product:Category'].astype(str)  # Ensure string type
        df['product:Price'] = pd.to_numeric(df['product:Price'], errors='coerce')  # Convert to float
        df['product:ProductID'] = pd.to_numeric(df['product:ProductID'], errors='coerce')  # Convert to integer
        df['product:ProductName'] = df['product:ProductName'].astype(str)  # Ensure string type
        df['shipment:ShippingAddress'] = df['shipment:ShippingAddress'].astype(str)  # Ensure string type
        df['shipment:ShippingDate'] = pd.to_datetime(df['shipment:ShippingDate'], errors='coerce')  # Convert to datetime
        df['row_key'] = df['row_key'].astype(str)  # Ensure string type
        return df
    except Exception as e:
        raise ValueError(f"Error in typecasting: {e}")

# Endpoint to load the DataFrame from HBase
@app.route('/dashboard', methods=['GET'])
def homepage():
    global dataframe

    if dataframe is None:
        return jsonify({"error": "DataFrame not loaded. Please visit /load to load data."}), 400

    try:
        # Top Customers
        top_customers = dataframe.groupby('customer:CustomerID').agg(
            CustomerName=('customer:Name', 'first'),
            Age=('customer:Age', 'first'),
            Country=('customer:Country', 'first'),
            TotalAmount=('order:TotalAmount', 'sum')
        ).sort_values(by='TotalAmount', ascending=False).head(5)
        top_customers_html = top_customers.to_html(classes='table table-striped')

        # Top Products
        top_products = dataframe.groupby('product:ProductID').agg(
            ProductName=('product:ProductName', 'first'),
            Category=('product:Category', 'first'),
            Price=('product:Price', 'first'),
            TotalAmount=('order:TotalAmount', 'sum')
        ).sort_values(by='TotalAmount', ascending=False).head(5)
        top_products_html = top_products.to_html(classes='table table-striped')

        # Lowest Sales Countries
        low_sales = dataframe.groupby('customer:Country').agg(
            TotalAmount=('order:TotalAmount', 'sum')
        ).sort_values(by='TotalAmount', ascending=True).head(5)
        low_sales_html = low_sales.to_html(classes='table table-striped')

        # Most Loyal Customers
        loyal_customers = dataframe.groupby('customer:CustomerID').agg(
            CustomerName=('customer:Name', 'first'),
            Age=('customer:Age', 'first'),
            Country=('customer:Country', 'first'),
            Orders=('order:OrderDate', 'count')
        ).sort_values(by='Orders', ascending=False).head(5)
        loyal_customers_html = loyal_customers.to_html(classes='table table-striped')

        # Sales Plot
        img_sales = io.BytesIO()
        plt.figure(figsize=(10, 6))
        dataframe.groupby('order:OrderDate')['order:TotalAmount'].sum().plot(kind='line', marker='o')
        plt.title('Datewise Sales')
        plt.ylabel('Total Revenue')
        plt.xlabel('Order Date')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(img_sales, format='png')
        img_sales.seek(0)
        plt.close()
        sales_chart = base64.b64encode(img_sales.getvalue()).decode('utf-8')

        # Pie Charts
        img_category = io.BytesIO()
        plt.figure(figsize=(10, 6))
        dataframe.groupby('product:Category')['order:TotalAmount'].sum().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Sales by Category')
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig(img_category, format='png')
        img_category.seek(0)
        plt.close()
        category_chart = base64.b64encode(img_category.getvalue()).decode('utf-8')

        img_country = io.BytesIO()
        plt.figure(figsize=(10, 6))
        dataframe.groupby('customer:Country')['order:TotalAmount'].sum().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Sales by Country')
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig(img_country, format='png')
        img_country.seek(0)
        plt.close()
        country_chart = base64.b64encode(img_country.getvalue()).decode('utf-8')

        # Render all in HTML
        html_template = f"""
        <html>
        <head><title>Data Analytics Dashboard</title></head>
        <body>
            <h1>Welcome to the Data Analytics Dashboard</h1>
            <h2>Top Customers</h2>
            {top_customers_html}
            <h2>Top Products</h2>
            {top_products_html}
            <h2>Lowest Sales by Country</h2>
            {low_sales_html}
            <h2>Most Loyal Customers</h2>
            {loyal_customers_html}
            <h2>Datewise Sales</h2>
            <img src="data:image/png;base64,{sales_chart}" alt="Datewise Sales">
            <h2>Sales by Category</h2>
            <img src="data:image/png;base64,{category_chart}" alt="Sales by Category">
            <h2>Sales by Country</h2>
            <img src="data:image/png;base64,{country_chart}" alt="Sales by Country">
        </body>
        </html>
        """

        return html_template
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def load_data():
    print('loading data')
    global dataframe
    try:
        # Connect to HBase Thrift Server
        connection = happybase.Connection(host=HBASE_HOST, port=HBASE_PORT)
        table = connection.table(TABLE_NAME)
        print('connection made')

        # ******* limit rows ***********

        start_row = request.args.get('start_row', None)  # Start row for pagination
        batch_size = int(request.args.get('batch_size', 1000))  # Default batch size to 100 rows


        rows = table.scan(row_start=start_row, limit=batch_size)
        data = [
            {**{k.decode('utf-8'): v.decode('utf-8') for k, v in row.items()}, 'row_key': key.decode('utf-8')}
            for key, row in rows
        ]

        # **************

        # rows = table.scan(batch_size=1000)  # Adjust batch size if needed
        # data = [
        #     {**{k.decode('utf-8'): v.decode('utf-8') for k, v in row.items()}, 'row_key': key.decode('utf-8')}
        #     for key, row in rows
        # ]


        dataframe = pd.DataFrame(data)

        # Typecast the DataFrame
        dataframe = typecast_dataframe(dataframe)

        # Render HTML with links to other endpoints
        html_template = """
        <html>
        <head><title>Data Loaded</title></head>
        <body>
            <h1>Data Loaded Successfully</h1>
            <p>DataFrame loaded and typecasted successfully with {rows} rows.</p>
            <nav>
            <ul>
                <li><a href="/dashboard">Dashboard</a></li>
                <li><a href="/product-search">Product Search</a></li>
            </ul>
            </nav>
        </body>
        </html>
        """.format(rows=len(dataframe))

        return render_template_string(html_template)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/product-search', methods=['GET', 'POST'])
def product_search():
    global dataframe
    if dataframe is None:
        return jsonify({"error": "DataFrame not loaded. Please visit /load first."}), 400

    if request.method == 'POST':
        product_name = request.form.get('product_name')
        if not product_name:
            return jsonify({"error": "Product name is required."}), 400

        try:
            # Filter data for the given product name
            product_data = dataframe[dataframe['product:ProductName'] == product_name]

            if product_data.empty:
                return jsonify({"error": "No data found for the given product name."}), 404

            # Summary statistics for the product
            monthly_revenue = product_data.groupby(product_data['order:OrderDate'].dt.to_period('M'))['order:TotalAmount'].sum()
            monthly_revenue_html = monthly_revenue.to_frame().to_html(classes='table table-striped')

            # Top 5 countries that order the product
            top_countries = product_data.groupby('customer:Country')['order:TotalAmount'].sum().sort_values(ascending=False).head(5)
            top_countries_html = top_countries.to_frame().to_html(classes='table table-striped')

            # Generate a bar chart for monthly revenue
            img_revenue = io.BytesIO()
            plt.figure(figsize=(10, 6))
            monthly_revenue.plot(kind='bar')
            plt.title(f'Monthly Revenue for {product_name}')
            plt.ylabel('Total Revenue')
            plt.xlabel('Month')
            plt.tight_layout()
            plt.savefig(img_revenue, format='png')
            img_revenue.seek(0)
            plt.close()
            revenue_chart = base64.b64encode(img_revenue.getvalue()).decode('utf-8')

            # Render HTML with form and results
            html_template = f"""
            <html>
            <head><title>Product Search</title></head>
            <body>
                <h1>Product Search</h1>
                <form method="post">
                    <label for="product_name">Product Name:</label>
                    <input type="text" id="product_name" name="product_name" required>
                    <button type="submit">Search</button>
                </form>
                <h2>Monthly Revenue for {product_name}</h2>
                {monthly_revenue_html}
                <img src="data:image/png;base64,{revenue_chart}" alt="Monthly Revenue Chart">
                <h2>Top 5 Countries that Order {product_name}</h2>
                {top_countries_html}
            </body>
            </html>
            """
            return render_template_string(html_template)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Render the search form
    html_template = """
    <html>
    <head><title>Product Search</title></head>
    <body>
        <h1>Product Search</h1>
        <form method="post">
            <label for="product_name">Product Name:</label>
            <input type="text" id="product_name" name="product_name" required>
            <button type="submit">Search</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(html_template)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)