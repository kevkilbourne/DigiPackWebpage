from pathlib import Path
import multiprocessing
import googlesearch
import shutil
import os
import pdfkit
from googlesearch import search




def searchingAlgorithm(textInput):
    #initalize variables
    webResults = []

    #For each website in the google search. Search on Google using the keywords that we provide
    for website in search(textInput, tld="com", num = 10, stop = 10, pause = 2):
        #Checks to see if the collected website is not a .pdf file already
        if('pdf' not in website):
            #If so, then it checks if the collected website is not a YouTube page
            if('youtube.com' not in website):
                #If so, adds the website to the results list
                webResults.append(website)

    return webResults

def downloadWebsites(links, path):

    BASE_DIR = Path(__file__).resolve().parent.parent
    print(BASE_DIR)
    index = 0
    websiteCount = 1
    websiteNames = []
    DirectPath = os.path.join(BASE_DIR, 'Assignments/' + path + '/')
    print(links)
    #Checks the length of the Results List
    numResults = len(links)
    if not os.path.exists(DirectPath):
        os.makedirs(DirectPath)
    #While the website number is less then the length of the results list
    while(websiteCount - 1 < numResults):
        #Appends a Resource_# to a website String used to name the file
        websiteNames.append("Resource_" + str(websiteCount))
        #increments WebsiteNumber by 1
        websiteCount += 1

    #For every website in the results list
    for website in links:
        #Checks if the WebsiteStrings is not equal to None
        if(websiteNames[index] != None):
            try:    
                print(f"Converting: {website}...")

                #Converts the html website into a pdf website

                # build a multithreaded process and start it
                process = multiprocessing.Process(target=downloadWebsite, args=(website, DirectPath + websiteNames[index] + '.pdf',))
                process.start()

                # wait for 10 seconds or until the site is downloaded
                process.join(10)

                # if site is not yet downloaded
                if process.is_alive():

                    # if its not finished yet, we will abort and move on
                    print("Download Timeout on " + website)

                    # kill the process
                    process.kill()

                    # rejoin threads
                    process.join()

                #This then downloads into the determined location
                #pdfkit.from_url(website, DirectPath + websiteNames[index] +'.pdf', verbose=True)

                #increments index
                index += 1

                print(f"Conversion Done!")

            # catch any errors by moving on
            except OSError as error:
                print("Failed to download " + website + "\nError: " + str(error))

def downloadWebsite(link, path):
    pdfkit.from_url(link, path)

