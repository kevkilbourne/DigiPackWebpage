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

def SearchingAlgorithm(post):
    #initalize variables
    index = 0;
    Query = []
    QueryString = ""
    WebsiteResult = []
    TextInput = ""
    PDFConversion = []
    DirectPath = os.path.expanduser("~")+"/Downloads/"
    DirectPath = DirectPath.replace('/', '\\')


    print('DIRECT PATH: ' + DirectPath)

    #Ask for input from the user
    TextInput = post

    #For each website in the google search. Search on Google using the keywords that we provide
    for Websites in search(TextInput, tld="com", num = 10, stop = 10, pause = 2):
        #Checks to see if the collected website is not a .pdf file already
        if('pdf' not in Websites):
            #If so, then it checks if the collected website is not a YouTube page
            if('youtube.com' not in Websites):
                #If so, adds the website to the results list
                WebsiteResult.append(Websites)

    return WebsiteResult


def DownloadWebsites(LinksList, path):

    BASE_DIR = Path(__file__).resolve().parent.parent
    print(BASE_DIR)
    index = 0
    WebsiteNumber = 1
    WebsiteStrings = []
    DirectPath = os.path.join(BASE_DIR, 'Assignments/' + path + '/') 
    print(LinksList)
    #Checks the length of the Results List
    LengthWebsiteResult = len(LinksList)
    if not os.path.exists(DirectPath):
        os.makedirs(DirectPath)
    #While the website number is less then the length of the results list
    while(WebsiteNumber-1 < LengthWebsiteResult):
        #Appends a Resource_# to a website String used to name the file
        WebsiteStrings.append("Resource_" + str(WebsiteNumber))
        #increments WebsiteNumber by 1
        WebsiteNumber += 1

    #For every website in the results list
    for Websites in LinksList:
        #Checks if the WebsiteStrings is not equal to None
        if(WebsiteStrings[index] != None):
           print(f"Converting: {Websites}...")

           #Converts the html website into a pdf website calling the file to the
           #correct numbering system in WebsiteStrings.
           #This then downloads into the same spot where this python file is located
           pdfkit.from_url(Websites, DirectPath + WebsiteStrings[index] +'.pdf')
           #Copies the file and sends it to a new destination
           #newPath = shutil.copy(WebsiteStrings[index]+'.pdf', 'DirectPath')
           #shutil.move(WebsiteStrings[index]+'.pdf', DirectPath)
           #Deletes the original pdf file
           #os.remove(WebsiteStrings[index]+'.pdf')
           #increments index
           index += 1

           print(f"Conversion Done!")
