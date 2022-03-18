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
import csv, datetime


def landing_page(request):
    return render(request, 'DigitalBackpack/LandingWebpage.html')


def student_page(request):

    # ----------------- Recording time and updating Heatmap .csv ----------------- #

    # Gathers time information
    current_datetime = datetime.datetime.now()
    day = current_datetime.weekday()
    hour = current_datetime.hour

    # Opens .csv file to be converted to 2D array
    with open("DigitalBackpack/static/csv/updated_timeframes.csv", newline='') as file:
        result_list = list(csv.reader(file))

    # Converts .csv to 2D array
    data_array = np.array(result_list)

    # datetime.weekday() provides weekdays as indexes (where 'day' = 0 through 6) starting with Monday
    # Finds the correct position within 2D array and sets value to 1 (meaning connection detected)
    if day == 0:
        data_array[hour][0] = 1
    elif day == 1:
        data_array[hour][1] = 1
    elif day == 2:
        data_array[hour][2] = 1
    elif day == 3:
        data_array[hour][3] = 1
    elif day == 4:
        data_array[hour][4] = 1
    elif day == 5:
        data_array[hour][5] = 1
    else:
        data_array[hour][6] = 1

    # Converts newly updated 2D array back into .csv file
    updated_timeframes = data_array
    with open("DigitalBackpack/static/csv/updated_timeframes.csv", "w+", newline='') as new_file:
        csv_writer = csv.writer(new_file, delimiter=',')
        csv_writer.writerows(updated_timeframes)

    file.close()
    new_file.close()

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


def connection_page(request):

    # ----------------- Creation of Heatmap ----------------- #

    # Gathers time information
    current_datetime = datetime.datetime.now()
    day = current_datetime.weekday()

    # Open .csv file and read
    try:
        dataset = read_csv("DigitalBackpack/static/csv/updated_timeframes.csv")
    except FileNotFoundError:
        dataset = read_csv("DigitalBackpack/static/csv/timeframes.csv")

    # Checking to see if recording the future date is necessary
    future_day = None
    if day == 6:
        future_day = (current_datetime + datetime.timedelta(weeks=1)).strftime("%d")

    # Sets flag that enables resetting of the heatmap
    new_week_flag = False
    if current_datetime.strftime("%d") == future_day:
        # Calculates new future date and sets it to a week in the future
        future_day = (current_datetime + datetime.timedelta(weeks=1)).strftime("%d")
        new_week_flag = True

    # If it is the reset day (Sunday) and it's been a weeks time, erase previous week's heatmap to start the week over
    if new_week_flag:
        dataset = read_csv("DigitalBackpack/static/csv/timeframes.csv")

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

