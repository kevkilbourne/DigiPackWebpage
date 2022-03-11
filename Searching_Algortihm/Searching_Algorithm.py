import googlesearch
import shutil
import os
import pdfkit
from googlesearch import search
#Finds where the executable program is
path_wkhtmltopdf = r'\DigitalBackpack\wkhtmltopdf\bin\wkhtmltopdf.exe'
#Sets the configurations to the path
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


def main():

    #initalize variables
    index = 0;
    Query = []
    QueryString = ""
    WebsiteResult = []
    TextInput = ""
    PDFConversion = []
    WebsiteNumber = 1
    WebsiteStrings = []
    DirectPath = os.path.expanduser("~")+"/Downloads/"

    #Ask for input from the user
    TextInput = request.GET['Keywords']

    #Adds the user's input and splits them into list for each comma used
    Query = TextInput.split(', ')

    #For each website in the google search. Search on Google using the keywords that we provide
    for Websites in search(TextInput, tld="com", num = 10, stop = 10, pause = 2):
        #Checks to see if the collected website is not a .pdf file already
        if('pdf' not in Websites):
            #If so, then it checks if the collected website is not a YouTube page
            if('youtube.com' not in Websites):
                #If so, adds the website to the results list
                WebsiteResult.append(Websites)

    #Checks the length of the Results List
    LengthWebsiteResult = len(WebsiteResult)

    #While the website number is less then the length of the results list
    while(WebsiteNumber-1 < LengthWebsiteResult):
        #Appends a Resource_# to a website String used to name the file
        WebsiteStrings.append("Resource_" + str(WebsiteNumber))
        #increments WebsiteNumber by 1
        WebsiteNumber += 1

    #Resets the index for its next use
    index = 0

    #For every website in the results list
    for Websites in WebsiteResult:
        #Checks if the WebsiteStrings is not equal to None
        if(WebsiteStrings[index] != None):
           #Converts the html website into a pdf website calling the file to the
           #correct numbering system in WebsiteStrings.
           #This then downloads into the same spot where this python file is located
           pdfkit.from_url(Websites, WebsiteStrings[index]+'.pdf', configuration=config)
           #Copies the file and sends it to a new destination
           newPath = shutil.copy(WebsiteStrings[index]+'.pdf', '/Users/jnati/Downloads/')
           #Deletes the original pdf file
           os.remove(WebsiteStrings[index]+'.pdf')
           #increments index
           index += 1
main()
