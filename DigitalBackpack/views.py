from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import sqlite3
import importlib
import numpy as np
import matplotlib.pyplot as plt, mpld3
import seaborn as sns
from pandas import read_csv
import DigitalBackpack.models as models
from .forms import RatingForm 

def student_page(request):
    return render(request, 'DigitalBackpack/StudentWebpage.html')

def teacher_page(request):
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

def connection_page(request):
    # Open .csv file and read
    dataset = read_csv("DigitalBackpack/static/csv/timeframes.csv")
    # print(dataset)

    # Sets up general heatmap attributes including size, title, and x and y axes
    plt.figure(figsize=(8, 8))
    # plt.title("Your Recent Connections")
    plt.xlabel("Days of the week", size=15)
    plt.ylabel("Time of day", size=15)

    # Creation of the heatmap with specific characteristics
    heatmap = sns.heatmap(dataset, linewidths=0.5, square=True, cmap=["#5d7682", "#38b6ff"], cbar=False)

    # Adjustments made to the heatmap's characteristics
    time_ticks = ["12:00AM", "1:00AM", "2:00AM", "3:00AM", "4:00AM", "5:00AM", "6:00AM", "7:00AM", "8:00AM", "9:00AM",
                  "10:00AM", "11:00AM", "12:00PM", "1:00PM", "2:00PM", "3:00PM", "4:00PM", "5:00PM", "6:00PM", "7:00PM",
                  "8:00PM", "9:00PM", "10:00PM", "11:00PM"]
    heatmap.invert_yaxis()
    plt.yticks(np.arange(24), time_ticks)  # Arranges 24 ticks and labels them with corresponding value in 'time_ticks'
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)

    # ----------------- Getting heatmap to browser ----------------- #

    # plt.savefig - Saves the figure as specified format for later usage
    complete_file = "DigitalBackpack/static/img/heatmap_timeframe.png"
    plt.savefig(complete_file, format='png')

    # mpld3.show() - Open figure in a web browser
    # Similar behavior to plt.show(). This opens the D3 visualization of the specified figure in the web browser.
    # On most platforms, the browser will open automatically
    # mpld3.show(heatmap, 'localhost')

    # mlpd3.save_html() - Saves a matplotlib figure to a html file
    # mpld3.save_html(heatmap, "timeframe_heatmap.html")

    # mlpd3.fig_to_html() - Outputs html representation of the figure
    # html_str = mpld3.fig_to_html(plt)
    # html_file = open("index.html", "w")
    # html_file.write(html_str)

    return render(request, 'DigitalBackpack/student_connectivity.html')
