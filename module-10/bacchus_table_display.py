import mysql.connector
from mysql.connector import errorcode
import dotenv
from dotenv import dotenv_values

def main():
    #Get secrets from .env file
    secrets = dotenv_values(".env")
    config = {"user": secrets["USER"], "password": secrets["PASSWORD"], "host": secrets["HOST"], "database": secrets["DATABASE"], "raise_on_warnings": True}
    
    try:
        #Connect to database
        database = mysql.connector.connect(**config)
        print("Connected to database")
        queries(database)
    
    except mysql.connector.Error as error:
        #Give error messages if connection fails
        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Invalid username or password")
        if error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist")
        else:
            print("An unknown error occurred")
    
    finally:
        #Close database connection
        database.close()

def queries(database):
    cursor = database.cursor()
    
    #Show the results from the Employees table
    cursor.execute("SELECT * FROM employees;")
    employees = cursor.fetchall()
    print("-- Employees Table --")
    for employee in employees:
        print(f"Employee ID:  {employee[0]}\nFirst Name: {employee[1]}\nLast Name: {employee[2]}\nPosition: {employee[3]}\nSupervisor ID: {employee[4]}\n")
    
    #Show the results from the Work Hours table
    cursor.execute("SELECT * FROM work_hours;")
    work_hours = cursor.fetchall()
    print("-- Work Hours Table --")
    for hours in work_hours:
        print(f"Work Hours ID: {hours[0]}\nEmployee ID: {hours[1]}\nDate: {hours[2]}\nHours Worked: {hours[3]}\n")
    
    #Show the results from the Supplies table
    cursor.execute("SELECT * FROM supplies;")
    supplies = cursor.fetchall()
    print("-- Supplies Table --")
    for supply in supplies:
        print(f"Supply ID: {supply[0]}\nName: {supply[1]}\nInventory Quantity: {supply[2]}\n")
    
    #Show the results from the Suppliers table
    cursor.execute("SELECT * FROM suppliers")
    suppliers = cursor.fetchall()
    print("-- Suppliers Table --")
    for supplier in suppliers:
        print(f"Supplier ID: {supplier[0]}\nName: {supplier[1]}\nState: {supplier[2]}\nCity: {supplier[3]}\nStreet Address: {supplier[4]}\nPhone Number: {supplier[5]}\nEmail: {supplier[6]}\n")
    
    #Show the results from the Supply Orders table
    cursor.execute("SELECT * FROM supply_orders;")
    orders = cursor.fetchall()
    print("-- Supply Orders Table --")
    for order in orders:
        print(f"Order ID: {order[0]}\nSupplier ID: {order[1]}\nSupply ID: {order[2]}\nQuantity: {order[3]}\nUnit Price: {order[4]}\nExpected Delivery Date: {order[5]}\nActual Delivery Date: {order[6]}\n")
    
    #Show the results from the Products table
    cursor.execute("SELECT * FROM products;")
    products = cursor.fetchall()
    print("-- Products Table --")
    for product in products:
        print(f"Product ID: {product[0]}\nName: {product[1]}\nPrice: {product[2]}\n")
    
    #Show the results from the Distributors table
    cursor.execute("SELECT * FROM distributors;")
    distributors = cursor.fetchall()
    print("-- Distributors Table --")
    for distributor in distributors:
        print(f"Distributor ID: {distributor[0]}\nName: {distributor[1]}\nState: {distributor[2]}\nCity: {distributor[3]}\nStreet Address: {distributor[4]}\nPhone Number: {distributor[5]}\nEmail: {distributor[6]}\n")
    
    #Show the results from the Product sales table
    cursor.execute("SELECT * FROM product_sales;")
    sales = cursor.fetchall()
    print("-- Product Sales Table --")
    for sale in sales:
        print(f"Sale ID: {sale[0]}\nProduct ID: {sale[1]}\nDistributor ID: {sale[2]}\nQuantity: {sale[3]}\n")

if __name__ == '__main__':# Conditionally executes the main function
    main()