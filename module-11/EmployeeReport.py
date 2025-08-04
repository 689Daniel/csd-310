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
    
    #selects all of the employees, their positions, their supervisors if applicable, and the sum of their work hours for each quarter.
    #Shows 0 if an employee has no work hours for a specific quarter
    cursor.execute("""SELECT CONCAT(employees.First_Name,' ', employees.Last_Name) AS Employee_Name, employees.Position, CONCAT(supervisors.First_Name, ' ', supervisors.Last_Name) AS Supervisor_Name,
        IFNULL(quarter4.Work_Hours, 0) AS Q4, IFNULL(quarter1.Work_Hours, 0) AS Q1, IFNULL(quarter2.Work_Hours, 0) AS Q2, IFNULL(quarter3.Work_Hours, 0) AS Q3
        FROM employees
        LEFT JOIN employees AS supervisors
        ON employees.Supervisor_ID = supervisors.Employee_ID
        LEFT JOIN (SELECT Employee_ID, SUM(Hours_Worked) AS Work_Hours
            FROM work_Hours
            WHERE Work_Hours_Date BETWEEN "2024-10-01" AND "2024-12-31"
            GROUP BY Employee_ID) AS quarter4
        ON employees.Employee_ID=quarter4.Employee_ID
        LEFT JOIN (SELECT Employee_ID, SUM(Hours_Worked) AS Work_Hours
            FROM work_Hours
            WHERE Work_Hours_Date BETWEEN "2025-01-01" AND "2025-03-30"
            GROUP BY Employee_ID) AS quarter1
        ON employees.Employee_ID=quarter1.Employee_ID
        LEFT JOIN (SELECT Employee_ID, SUM(Hours_Worked) AS Work_Hours
            FROM work_Hours
            WHERE Work_Hours_Date BETWEEN "2025-04-01" AND "2025-06-30"
            GROUP BY Employee_ID) AS quarter2
        ON employees.Employee_ID=quarter2.Employee_ID
        LEFT JOIN (SELECT Employee_ID, SUM(Hours_Worked) AS Work_Hours
            FROM work_Hours
            WHERE Work_Hours_Date BETWEEN "2025-07-01" AND "2025-09-30"
            GROUP BY Employee_ID) AS quarter3
        ON employees.Employee_ID=quarter3.Employee_ID;""")
    employee_data = cursor.fetchall()
    
    #Displays query results
    print("-- Quarterly Report of Employee Work Hours --")
    for employee in employee_data:
        print(f"Name:                   {employee[0]}")
        print(f"Position:               {employee[1]}")
        if employee[2]:#Only displays the supervisor field if it exists
            print(f"Supervisor:             {employee[2]}")
        print(f"Q4 (2024) Work Hours:   {employee[3]}")
        print(f"Q1 Work Hours:          {employee[4]}")
        print(f"Q2 Work Hours:          {employee[5]}")
        print(f"Q3 Work Hours:          {employee[6]}")
        print()
        

if __name__ == '__main__':# Conditionally executes the main function
    main()