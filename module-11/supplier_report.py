import mysql.connector
from mysql.connector import errorcode
import dotenv
from dotenv import dotenv_values

def main():
    secrets = dotenv_values(".env")
    config = {"user": secrets["USER"], "password": secrets["PASSWORD"], "host": secrets["HOST"], "database": secrets["DATABASE"], "raise_on_warnings": True}
    
    try:
        database = mysql.connector.connect(**config)
        print("Connected to database")
        queries(database)
    
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Invalid username or password")
        if error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist")
        else:
            print("An unknown error occurred")
    
    finally:
        database.close()

def queries(database):
    cursor = database.cursor()
    
    #Selects all of the suppliers
    cursor.execute("""SELECT Supplier_ID, Name, State, City, Street_Address, Phone_Number, Email
        FROM suppliers
        ORDER BY Supplier_ID;""")
    supplier_data = cursor.fetchall()
    
    #Prints the suppliers query
    print("-- Supplier Contact Information Report --")
    for supplier in supplier_data:
        print(f"Supplier ID:            {supplier[0]}")
        print(f"Name:                   {supplier[1]}")
        print(f"State:                  {supplier[2]}")
        print(f"City:                   {supplier[3]}")
        print(f"Street Address:         {supplier[4]}")
        print(f"Phone Number:           {supplier[5]}")
        print(f"Email:                  {supplier[6]}")
        print()
    
    #Selects all of the orders, as well as the difference between their actual and expected dates, ordered by the supplier
    cursor.execute("""SELECT Order_ID, suppliers.Name AS "Supplier Name", supplies.Name AS "Supplies", Quantity, Unit_Price, (Quantity * Unit_Price) AS "Order Total", Expected_Delivery_Date, Actual_Delivery_Date, DATEDIFF(Actual_Delivery_Date, Expected_Delivery_Date) AS "Arrival Time"
        From supply_orders
        INNER JOIN suppliers ON suppliers.Supplier_ID = supply_orders.Supplier_ID
        INNER JOIN supplies ON supplies.Supply_ID = supply_orders.Supply_ID
        ORDER BY suppliers.Name;""")
    Orders = cursor.fetchall()
    
    #Prints the orders query
    print("-- Report of Order Dates --")
    for order in Orders:
        print(f"Order ID:               {order[0]}")
        print(f"Supplier:               {order[1]}")
        print(f"Supply:                 {order[2]}")
        print(f"Quantity:               {order[3]}")
        print(f"Unit Price:             ${order[4]:.2f}")
        print(f"Order Total:            ${order[5]:.2f}")
        print(f"Expected Delivery Date: {order[6]}")
        print(f"Actual Delivery Date:   {order[7]}")
        print(f"Difference:             {format_difference(order[8])}")
        print()
        
def format_difference(difference):#Formats the results of the difference between the actual and expected delivery date
    if difference > 0:
        return f"{difference} Days Late"
    elif difference < 0:
        return f"{difference * -1} Days Early"
    elif difference == 0:
        return "On Time"

if __name__ == '__main__':
    main()