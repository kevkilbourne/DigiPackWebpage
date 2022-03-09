from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import sqlite3
import importlib
import DigitalBackpack.models as models
from .forms import RatingForm 

def studentpage(request):
    return render(request, 'DigitalBackpack/StudentWebpage.html')

def teacherpage(request):
    return render(request, 'DigitalBackpack/TeacherWebpage.html')


def ratings(request): 
    # if we've received input for loading into the db
    if request.method == 'POST':
        # initialize loading variables
        input = request.POST
        
        # call our model submission
        success = models.submitRatings(input)

        # redirect our student back to their homepage
        return redirect('student_page')

    else:
        # grab our sites
        ratingSites = request.GET
        form = RatingForm(None, sites=ratingSites)


        # if they are sent via get to send ratings, give them the page
        return render(request, 'DigitalBackpack/Ratings.html', {'form': form})

def searching_algorithm(request):
    #initalize variables
    index = 0;
    Query = []
    QueryString = ""
    WebsiteResult = []
    TextInput = ""
    PDFConversion = []
    WebsiteNumber = 1
    WebsiteStrings = []
    DirectPath = 'Users\jnati\Downloads'

    #Ask for input from the user
    TextInput = input()

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
    #print(LengthWebsiteResult)

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

    return render(request, 'DigitalBackpack/TeacherWebpage.html')
