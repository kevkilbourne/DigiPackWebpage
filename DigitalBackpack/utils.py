from pathlib import Path
from django.contrib.auth.models import User
import multiprocessing
import googlesearch
import shutil
import os
import pdfkit
from googlesearch import search
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image
import numpy as np
import seaborn as sns
from pandas import read_csv
import datetime, csv

def makeHeatmap(username):
    # ----------------- Recording time and updating Heatmap .csv ----------------- #

    # Gathers time information
    current_datetime = datetime.datetime.now()
    day = current_datetime.weekday()  # provides weekdays as indexes (where 'day' = 0 through 6) starting with Monday
    hour = current_datetime.hour

    # Get student username and path to their Heatmap
    student_username = username
    student_heatmap_path = 'DigitalBackpack/static/Users/Students/student_' + student_username
    display_heatmap_csv = student_heatmap_path + '/' + student_username + '_display_heatmap.csv'
    working_heatmap_csv = student_heatmap_path + '/' + student_username + '_working_heatmap.csv'

    # Will grab empty, unused csv if student is created without file creation
    with open('DigitalBackpack/static/csv/empty_weekly.csv', newline='') as empty_file:
        weekly_result_list = list(csv.reader(empty_file))
    working_data_array = np.array(weekly_result_list)
    display_data_array = np.array(weekly_result_list)
    result_data_array = np.array(weekly_result_list)

    try:
        # Opens the student's display .csv file to be converted to 2D array
        with open(display_heatmap_csv, newline='') as display_file:
            display_result_list = list(csv.reader(display_file))
        display_data_array = np.array(display_result_list)  # Converts student's display .csv to 2D array
    except FileNotFoundError:
        print("Display File not found")

    try:
        # Opens the student's working .csv file to be converted to 2D array
        with open(working_heatmap_csv, newline='') as working_file:
            working_result_list = list(csv.reader(working_file))
        working_data_array = np.array(working_result_list)  # Converts student's working .csv to 2D array
    except FileNotFoundError:
        print("Working File not found")

    try:
        # Opens the empty result .csv file to be converted to 2D array
        with open('DigitalBackpack/static/csv/empty_weekly.csv', newline='') as result_file:
            result_list = list(csv.reader(result_file))
        result_data_array = np.array(result_list)  # Converts student's working .csv to 2D array
    except FileNotFoundError:
        print("Result File not found")

    working_data_array = updateWorkingHeatmap(working_data_array)

    # ----------------- Adding Working .csv file's data into Display .csv file ----------------- #
    result_data_array = transferWorkingData(working_data_array, display_data_array, result_data_array)

    # Copying the Result file back into the Display file
    display_data_array = result_data_array.copy()

    # Resetting the Working csv file to all 0s
    working_data_array = np.array(weekly_result_list)

    # ----------------- Conversion of 2D arrays back into .csv files ----------------- #

    try:
        # Converts newly updated display 2D array back into .csv file
        updated_display = display_data_array
        with open(display_heatmap_csv, "w+", newline='') as new_display_file:
            csv_writer = csv.writer(new_display_file, delimiter=',')
            csv_writer.writerows(updated_display)
    except FileNotFoundError:
        print("Display File not found when trying to write to file")

    try:
        # Converts newly updated working 2D array back into .csv file
        updated_working = working_data_array
        with open(working_heatmap_csv, "w+", newline='') as new_working_file:
            csv_writer = csv.writer(new_working_file, delimiter=',')
            csv_writer.writerows(updated_working)
    except FileNotFoundError:
        print("Working File not found when trying to write to file")

    empty_file.close()
    display_file.close()
    working_file.close()
    result_file.close()
    new_display_file.close()
    new_working_file.close()

    # ----------------- Creation of Heatmap ----------------- #

    # Gathers time information
    current_datetime = datetime.datetime.now()
    day = current_datetime.weekday()

    display_heatmap_csv = student_heatmap_path + '/' + student_username + '_display_heatmap.csv'
    working_heatmap_csv = student_heatmap_path + '/' + student_username + '_working_heatmap.csv'

    # Open weekly .csv file and read
    try:
        display_dataset = read_csv(display_heatmap_csv)
    except FileNotFoundError:
        display_dataset = read_csv("DigitalBackpack/static/csv/empty_weekly.csv")

    # Sets up general heatmap attributes including size and x and y axes
    plt.figure(figsize=(8, 8))
    plt.xlabel("Days of the week", size=15)
    plt.ylabel("Time of day", size=15)

    # Customizing the colormap colors (left value = lightest, right value = darkest)
    colormap = LinearSegmentedColormap.from_list('connection cmap', ['#99dcfc', '#448cbc'], N=100)

    # Creation of the heatmap with specific characteristics
    weekly_heatmap = sns.heatmap(display_dataset, linewidths=0.75, square=True, cmap=colormap)

    # Adjustments made to the heatmap's characteristics
    day_ticks = ["Mon.", "Tues.", "Wed.", "Thurs.", "Fri.", "Sat", "Sun"]
    time_ticks = ["12:00AM", "1:00AM", "2:00AM", "3:00AM", "4:00AM", "5:00AM", "6:00AM", "7:00AM", "8:00AM", "9:00AM",
                  "10:00AM", "11:00AM", "12:00PM", "1:00PM", "2:00PM", "3:00PM", "4:00PM", "5:00PM", "6:00PM", "7:00PM",
                  "8:00PM", "9:00PM", "10:00PM", "11:00PM"]

    weekly_heatmap.invert_yaxis()
    plt.yticks(np.arange(24), time_ticks)  # Arranges 24 y-axis ticks from 'time_ticks'
    plt.yticks(rotation=0)
    plt.yticks(np.arange(0, 24, 4))
    plt.xticks(np.arange(7), day_ticks)  # Arranges 7 x-axis ticks from 'day_ticks'
    plt.xticks(rotation=45)

    # plt.savefig - Saves the figure as specified format for later usage
    complete_file_path = student_heatmap_path + "/" + student_username + "_display_heatmap.png"
    plt.savefig(complete_file_path, format='png')

    # Cropping the Heatmap image
    heatmap_img = Image.open(complete_file_path)
    dimensions = (325, 75, 700, 775)
    img = heatmap_img.crop(dimensions)
    img = img.save(complete_file_path)


# Working Heatmap Data Input
# Finds the correct position within working 2D array and sets value to 1 (meaning connection detected)
def updateWorkingHeatmap(data_array):

    # Gathers time information
    current_datetime = datetime.datetime.now()
    day = current_datetime.weekday()  # provides weekdays as indexes (where 'day' = 0 through 6) starting with Monday
    hour = current_datetime.hour

    working_data_array = data_array

    if day == 0:
        working_data_array[hour][0] = 1
    elif day == 1:
        working_data_array[hour][1] = 1
    elif day == 2:
        working_data_array[hour][2] = 1
    elif day == 3:
        working_data_array[hour][3] = 1
    elif day == 4:
        working_data_array[hour][4] = 1
    elif day == 5:
        working_data_array[hour][5] = 1
    else:
        working_data_array[hour][6] = 1

    return working_data_array

def transferWorkingData(working_array, display_array, result_array):

    working_data_array = working_array
    display_data_array = display_array
    result_data_array = result_array

    # Adding working and display values together, placing them in temp result array
    for row in range(len(working_data_array)):
        for col in range(len(working_data_array[0])):
            result_data_array[row][col] = int(display_data_array[row][col]) + int(working_data_array[row][col])

    return result_data_array

def searchingAlgorithm(textInput):
    #initalize variables
    webResults = []

    # For each website in the google search. Search on Google using the keywords that we provide
    for website in search(textInput, tld="com", num = 10, stop = 10, pause = 2):
        # Checks to see if the collected website is not a .pdf file already
        if('pdf' not in website):
            # If so, then it checks if the collected website is not a YouTube page
            if('youtube.com' not in website):
                # If so, adds the website to the results list
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

