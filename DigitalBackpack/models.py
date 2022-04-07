from django.db import models
import sqlite3
from django.utils import timezone
from django.contrib.auth.models import User
from pathlib import Path

import googlesearch
import shutil
import os
import pdfkit
from googlesearch import search

class Teachers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first = models.CharField(max_length=100)
    last = models.CharField(max_length=100)
    classname = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username + " - " + self.classname

class Students(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField()
    classname = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    first = models.CharField(max_length=100, blank=True)
    last = models.CharField(max_length=100, blank=True)
    flagged = models.BooleanField(default=False)

    def __str__(self):
        return self.email + " - " + self.classname.classname

class Assignments(models.Model):
    title = models.CharField(max_length=100)
    dueDate = models.DateTimeField()
    instructions = models.TextField(blank=True)
    classname = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to="Assignments/", blank=True)

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
            print("Key: " + key)
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
