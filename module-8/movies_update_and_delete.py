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
                                                                                           
        
        #Display initial films table
        cursor=db.cursor()
        show_films(cursor, "DISPLAYING FILMS")
        
        cursor.execute("""INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)
            VALUES('Jurassic Park', 1993, 127, 'Steven Spielberg', 3, 2);""")
        show_films(cursor, "DISPLAYING FILMS AFTER INSERT")
        #Add Jurassic Park and show films table and show results
        
        cursor.execute("""UPDATE film
            SET genre_id=1
            WHERE film_name='Alien';""")
        show_films(cursor, "DISPLAYING FILMS AFTER UPDATING ALIEN TO HORROR")
        #Set Alien to horror and show results
        
        cursor.execute("""DELETE FROM film
            WHERE film_name='Gladiator';""")
        show_films(cursor, "DISPLAYING FILMS AFTER DELETING GLADIATOR")
        #Delete Gladiator and show results

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

def show_films(cursor, title):
    cursor.execute("""SELECT film_name AS 'Name', film_director AS 'Director', genre_name AS 'Genre', studio_name AS 'Studio'
        FROM film
        INNER JOIN genre ON genre.genre_id=film.genre_id
        INNER JOIN studio ON studio.studio_id=film.studio_id;""")
    movies = cursor.fetchall()
    #gets film, director, studio, and genre
    
    print(f"\n-- {title} --")
    for movie in movies:
        print(f"Film Name: {movie[0]}\nDirector: {movie[1]}\nGenre Name: {movie[2]}\nStudio Name: {movie[3]}\n")
       #prints formatted query results


if __name__ == '__main__':
    main()