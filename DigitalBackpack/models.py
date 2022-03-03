from django.db import models
import sqlite3

# Create your models here.


def submitRatings(post):
    # initialize function variables
    print(post)
    sql = None
    cursor = None
    dataTuple = None
    rating = 0
    count = 0
    RATING = 0
    NUM_RATINGS = 1
    SQL_TABLES_QUERY = """CREATE TABLE
                          IF NOT EXISTS WebRatings
                          (website TEXT NOT NULL,
                          rating REAL NOT NULL,
                          numRatings INTEGER NOT NULL)
                       """
    SQL_INSERT_QUERY = """INSERT INTO WebRatings
                          (website, rating, numRatings)
                          VALUES(?,?,?)
                       """
    SQL_SELECT_QUERY = """SELECT rating, numRatings
                          FROM WebRatings
                          WHERE website =?
                       """
    SQL_UPDATE_QUERY = """UPDATE WebRatings
                          SET rating = ?, numRatings = ?
                          WHERE website = ?
                       """
                    

    # connect to and initialize database
    try:
        sql = sqlite3.connect('Databases/WebsiteDB.db')
        cursor = sql.cursor()

        # if the table doesn't exist, create it
        cursor.execute(SQL_TABLES_QUERY)

    # catch any errors that may occur
    except sqlite3.Error as error:
        print("Unable to access database", error)
        return False

    # loop through all of  the received ratings
    for key in post.keys():
        try:
            # perform key validity checking
            if '.' in key:
            
                # pull query from the database, if it exists
                cursor.execute(SQL_SELECT_QUERY, (key,))
                dataTuple = cursor.fetchall()

                # see if we yielded any results
                if not dataTuple:
                    # if we did not, create a new entry for it
                    cursor.execute(SQL_INSERT_QUERY, (key, float(post.get(key)), 1,))

                    # indicate this addition to the database
                    print(key + " rating initialized to WebRatings Database: " + str(post.get(key)) + "(1)")
                
                else:
                    # reset our data tuple to the information inside, since we know it is present
                    dataTuple = dataTuple[0]

                    # recalculate the rating and set it equal to the new value
                    rating = (dataTuple[RATING] * dataTuple[NUM_RATINGS] + float(post.get(key))) / (dataTuple[NUM_RATINGS] + 1)

                    # update to database
                    cursor.execute(SQL_UPDATE_QUERY, (rating, dataTuple[NUM_RATINGS] + 1, key,))
                    # indicate result to debug
                    print(key + " rating updated in WebRatings Database: " + str(rating) + "(" + str(dataTuple[NUM_RATINGS] + 1) + ")")

                # commit our changes
                sql.commit()
        except sqlite3.Error as error:
            print("Connection to Website Rating Database lost during transaction", error)
            return False

    return True
