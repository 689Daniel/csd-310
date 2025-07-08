def main():
    #Copied from SQL test assignment
    """ import statements """
    import mysql.connector  # to connect
    from mysql.connector import errorcode

    import dotenv  # to use .env file
    from dotenv import dotenv_values

    # using our .env file
    secrets = dotenv_values(".env")

    """ database config object """
    config = {
        "user": secrets["USER"],
        "password": secrets["PASSWORD"],
        "host": secrets["HOST"],
        "database": secrets["DATABASE"],
        "raise_on_warnings": True  # not in .env file
    }

    try:
        """ try/catch block for handling potential MySQL database errors """

        db = mysql.connector.connect(**config)  # connect to the movies database

        # output the connection status
        print("\n  Database user {} connected to MySQL on host {} with database {}\n".format(config["user"], config["host"],
                                                                                           config["database"]))

        queries(db)#Executes queries

    except mysql.connector.Error as err:
        """ on error code """

        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("  The supplied username or password are invalid")

        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("  The specified database does not exist")

        else:
            print(err)

    finally:
        """ close the connection to MySQL """

        db.close()
#End copied code

def queries(db):
    cursor = db.cursor()

    #Display all records from studio table
    cursor.execute("SELECT * FROM studio;")
    studios = cursor.fetchall()
    print("--DISPLAYING studio RECORDS--")
    for studio in studios:
        print(f"Studio ID: {studio[0]}\nStudio Name: {studio[1]}\n")
    
    #Display all records from genre table
    cursor.execute("SELECT * FROM genre;")
    genres = cursor.fetchall()
    print("--DISPLAYING genre RECORDS--")
    for genre in genres:
        print(f"Genre ID: {genre[0]}\nGenre Name: {genre[1]}\n")
    
    #Display all films with a runtime of less than 2 hours
    cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120;")
    short_film = cursor.fetchall()
    print("--DISPLAYING short film RECORDS--")
    for film in short_film:
        print(f"Film Name: {film[0]}\nRuntime: {film[1]}\n")
    
    #Display all films, sorted by director
    cursor.execute("SELECT film_name, film_director FROM film ORDER BY film_director;")
    films = cursor.fetchall()
    print("--DISPLAYING director RECORDS in order--")
    for film in films:
        print(f"Film Name: {film[0]}\nDirector: {film[1]}\n")

if __name__ == '__main__':
    main()