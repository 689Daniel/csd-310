#Melissa Favelli, Jeremy Ginter, Daniel Preller
#Assignment 10.0
#27 July 2025

import mysql.connector
from mysql.connector import errorcode
import dotenv
from dotenv import dotenv_values

secrets = dotenv_values(".env")
config = {"user": secrets["USER"], "password": secrets["PASSWORD"], "host": secrets["HOST"],
          "database": secrets["DATABASE"], "raise_on_warnings": False}
try:
    # Connect to database
    db = mysql.connector.connect(**config)
    print("Connected to database")
    cursor = db.cursor()

    # Drops Tables
    cursor.execute("DROP TABLE IF EXISTS product_sales")
    cursor.execute("DROP TABLE IF EXISTS distributors")
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("DROP TABLE IF EXISTS work_hours")
    cursor.execute("DROP TABLE IF EXISTS employees")
    cursor.execute("DROP TABLE IF EXISTS supply_orders")
    cursor.execute("DROP TABLE IF EXISTS suppliers")
    cursor.execute("DROP TABLE IF EXISTS supplies")

    # Create Products Table
    cursor.execute("CREATE TABLE products(Product_ID int NOT NULL AUTO_INCREMENT, Name varchar(255) NOT NULL, "
                   "Price DECIMAL(6,2) NOT NULL, CONSTRAINT PK_Products PRIMARY KEY (Product_ID));")

    # Create Distributors
    cursor.execute("CREATE TABLE distributors (Distributor_ID int NOT NULL AUTO_INCREMENT,Name varchar(255) NOT NULL,"
                   "State varchar(255) NOT NULL,City varchar(255) NOT NULL, Street_Address varchar(255) NOT NULL,"
                   "Phone_Number varchar(12),Email varchar(255),CONSTRAINT PK_Distributors PRIMARY KEY ("
                   "Distributor_ID));")

    # Create product_sales table
    cursor.execute("CREATE TABLE product_sales (Sale_ID int NOT NULL AUTO_INCREMENT,Product_ID int NOT NULL,"
                   "Distributor_ID int NOT NULL,Quantity int NOT NULL,CONSTRAINT PK_Product_Sales PRIMARY KEY ("
                   "Sale_ID),CONSTRAINT FK_Product_Sales_Products FOREIGN KEY (Product_ID) REFERENCES products("
                   "Product_ID),CONSTRAINT FK_Product_Sales_Distributors FOREIGN KEY (Distributor_ID) REFERENCES "
                   "distributors(Distributor_ID));")


    # Create employees table
    cursor.execute("CREATE TABLE employees (Employee_ID int NOT NULL AUTO_INCREMENT, First_Name varchar(255) "
                   "NOT NULL,Last_Name varchar(255) NOT NULL,Position varchar(255) NOT NULL,Supervisor_ID int,"
                   "CONSTRAINT PK_Employees PRIMARY KEY (Employee_ID),CONSTRAINT FK_Supervisor FOREIGN KEY ("
                   "Supervisor_ID)"
                   "REFERENCES employees(Employee_ID));")



    # Creates work_hours table
    cursor.execute("CREATE TABLE work_hours (Work_Hours_ID int NOT NULL AUTO_INCREMENT,Employee_ID int NOT NULL,"
                   "Work_Hours_Date date NOT NULL,Hours_Worked FLOAT NOT NULL,CONSTRAINT PK_Work_Hours "
                   "PRIMARY KEY (Work_Hours_ID),CONSTRAINT FK_Work_Hours_Employees FOREIGN KEY (Employee_ID) "
                   "REFERENCES employees(Employee_ID));")


    #Creates suppliers table
    cursor.execute("CREATE TABLE suppliers (Supplier_ID int NOT NULL AUTO_INCREMENT, Name varchar(255) NOT NULL, "
                   "State varchar(255) NOT NULL, City varchar(255) NOT NULL, Street_Address varchar(255) NOT NULL, "
                   "Phone_Number varchar(255) NOT NULL, Email varchar(255) NOT NULL, "
                   "CONSTRAINT PK_Suppliers PRIMARY KEY (Supplier_ID));")


    #Creates supplies table
    cursor.execute("CREATE TABLE supplies(Supply_ID int NOT NULL AUTO_INCREMENT, Name varchar(255) NOT NULL, "
                   "Inventory_Quantity int NOT NULL, CONSTRAINT PK_Supplies PRIMARY KEY (Supply_ID));")


    #Creates supply_orders table
    cursor.execute("CREATE TABLE supply_orders(Order_ID int NOT NULL AUTO_INCREMENT, Supplier_ID int NOT NULL, "
                   "Supply_ID int NOT NULL, Quantity int NOT NULL, Unit_Price FLOAT NOT NULL, Expected_Delivery_Date "
                   "date NOT NULL, Actual_Delivery_Date date NOT NULL, "
                   "CONSTRAINT PK_Supply_Orders PRIMARY KEY (Order_ID), "
                   "CONSTRAINT FK_Supplier_ID FOREIGN KEY (Supplier_ID) REFERENCES suppliers(Supplier_ID), "
                   "CONSTRAINT FK_Supply_ID FOREIGN KEY (Supply_ID) REFERENCES supplies(Supply_ID));")


    # Populate Products Table
    cursor.execute("INSERT INTO products (Name, Price) VALUES"
                   "('Merlot', 69.99),"
                   "('Cabernet', 89.99),"
                   "('Chablis', 109.99),"
                   "('Chardonnay', 79.99);")

    # Populate Distributors Table
    cursor.execute("INSERT INTO distributors (Name, State, City, Street_Address, Phone_Number, Email) VALUES"
                   "('Total Wine', 'Oregon', 'Portland', '123 SW 1st Street', '+15031234567', 'totalwine@email.com'),"
                   "('Costco', 'California', 'Los Angeles', '321 N 2nd Street', '+13131234567', "
                   "'costcowine@costco.com'),"
                   "('Fred Meyer', 'New York', 'New York City', '456 SW 3rd Street', '+12121234567', "
                   "'fredmeyerwine@fredmeyer.com'),"
                   "('Safeway', 'California', 'Los Angeles', '456 NW 4th Street', '+13134567890', "
                   "'safewaywine@safeway.com'),"
                   "('Walmart', 'California', 'Los Angeles', '789 NE 5th Street', '+13137890123', "
                   "'walmartwine@walmart.com'),"
                   "('Target', 'New York', 'New York City','101 S 6th Street', '+12121011121', "
                   "'targetwine@target.com');")

    # Populate product_sales table
    cursor.execute("INSERT INTO product_sales (Product_ID, Distributor_ID, Quantity) VALUES"
                   "(1, 1, 30),"
                   "(1,2,60),"
                   "(2,3,100),"
                   "(2,4,20),"
                   "(3,5,120),"
                   "(4,6,70);")

    # Populate Employees Table
    cursor.execute("INSERT INTO employees (First_Name, Last_Name, Position, Supervisor_ID) VALUES"
                   "('Stan', 'Bacchus', 'Owner', NULL),"
                   "('Davis', 'Bacchus', 'Owner', NULL),"
                   "('Janet', 'Collins', 'Payroll', 1),"
                   "('Roz', 'Murphy', 'Marketing', 2),"
                   "('Bob', 'Ulrich', 'Marketing Assistant', 4),"
                   "('Henry', 'Doyle', 'Production', 1)")
    # Populate work_hours Table
    cursor.execute("INSERT INTO work_hours (Employee_ID, Work_Hours_Date, Hours_Worked) VALUES"
                   "(1, '2025-07-27', 8),"
                   "(2, '2025-07-27', 8),"
                   "(3, '2025-07-27', 7.5),"
                   "(4, '2025-07-27', 4.5),"
                   "(5, '2025-07-27', 4),"
                   "(6, '2025-07-27', 8);")
    # Populate suppliers table
    cursor.execute("INSERT INTO suppliers (Name, State, City, Street_Address, Phone_Number, Email) VALUES"
                   "('Wine Supply', 'California', 'Los Angeles', '111 NW 7th St', '+12121034001', "
                   "'winesupply@gmail.com'),"
                   "('Napa Supply', 'California', 'Napa', '555 NW 11th St', '+12120987654', 'contact@napasupply.com'),"
                   "('Wine Stuff', 'California', 'Napa', '667 NW 12th St', '+12120985678', 'getstuff@winestuff.com');")
    # Populates supplies table
    cursor.execute("INSERT INTO supplies (Name, Inventory_Quantity) VALUES"
                   "('Bottles', 200),"
                   "('Corks', 200),"
                   "('Labels', 200),"
                   "('Boxes', 50),"
                   "('Vats', 20),"
                   "('Tubing', 50);")

    # Populates supply_orders table
    cursor.execute("INSERT INTO supply_orders(Supplier_ID, Supply_ID, Quantity, Unit_Price, Expected_Delivery_Date, Actual_Delivery_Date) VALUES"
                   "(1, 1, 100, 1.5, '2025-06-15','2025-06-15'),"
                   "(1, 2, 100, 0.5, '2025-06-15','2025-06-15'),"
                   "(2, 3, 100, 0.1, '2025-06-30','2025-06-30'),"
                   "(2, 4, 25, 2.5, '2025-07-01','2025-06-01'),"
                   "(3, 5, 10, 20.5, '2025-07-10','2025-07-20'),"
                   "(3, 5, 20, 10, '2025-07-10','2025-07-25');")

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

