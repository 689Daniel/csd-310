import mysql.connector
from mysql.connector import errorcode
import dotenv
from dotenv import dotenv_values

secrets = dotenv_values(".env")
config = {"user": secrets["USER"], "password": secrets["PASSWORD"], "host": secrets["HOST"],
          "database": secrets["DATABASE"], "raise_on_warnings": True}
try:
    # Connect to database
    db = mysql.connector.connect(**config)
    print("Connected to database")
    cursor = db.cursor()

    # Selects all Wines, the Distributors, and the Sales of that wine to that distributor.
    cursor.execute("SELECT products.Name AS ProductName, distributors.Name AS DistributorName, product_sales.Quantity FROM "
                   "product_sales JOIN products ON product_sales.Product_ID = products.product_ID JOIN distributors ON "
                   "product_sales.Distributor_ID = distributors.distributor_ID;")

    sales_data = cursor.fetchall()

    print("-- Wine Distribution --")
    for sales in sales_data:
        print(f"Wine: {sales[0] }")
        print(f"Distributor: {sales[1]}")
        print(f"Quantity: {sales[2]}")
        print(" ")
except mysql.connector.Error as error:
    # Give error messages if connection fails
    if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Error: Invalid username or password")
    if error.errno == errorcode.ER_BAD_DB_ERROR:
        print("Error: Database does not exist")
    else:
        print("An unknown error occurred", error)
finally:
    # Close database connection
    db.commit()
    db.close()

