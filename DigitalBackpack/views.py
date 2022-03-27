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
from .forms import RatingForm, TeacherRegistrationForm, ClassRegistrationForm, AddStudentForm, StudentRegistrationForm, StudentAccountCompletionForm, AssignmentForm
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login

from DigitalBackpack.forms import SearchingALgorithmForm


# group_required helper decorator
#
# ensure's a user is authenticated and present in a group in order to access certain views
# returns a boolean True or False correlated to their user access
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups, login_url='landing_page')

# landing page view
#
# primary landing page for digital backpack
def landing_page(request):
    return render(request, 'DigitalBackpack/LandingWebpage.html')

# login reroute view
#
# invisible view by which the system can check group permissions to decide where a user will be
# routed upon login
def login_reroute(request):
    # redirect to teacher page
    print("Groups:")
    print(str(User.objects.get(id=request.session.get('_auth_user_id')).groups.first()))
    if str(User.objects.get(id=request.session.get('_auth_user_id')).groups.first()) == "Teachers":
        return redirect('teacher_page')

    elif str(User.objects.get(id=request.session.get('_auth_user_id')).groups.first()) == "Students":
        return redirect('student_page')

    else:
        return redirect('landing_page')
    
# student page view
#
# returns student homepage
@group_required('Students')
def landing_page(request):
    return render(request, 'DigitalBackpack/LandingWebpage.html')

def student_page(request):
    return render(request, 'DigitalBackpack/StudentWebpage.html')

def teacher_page(request):
    return render(request, 'DigitalBackpack/TeacherWebpage.html')

def get_add_assignment_page(request):

    if request.method == 'GET':
        form = SearchingALgorithmForm()
        return render(request, 'DigitalBackpack/AssignmentWebpage.html', {'form': form})

    else:
        if 'GrabWebsite' in request.POST:
            form = SearchingALgorithmForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data['post']

            input = form['post'].value()

            print(input)


            # loop through our remaining form items
            for studentEmail in form:
                # see if this user already has an account present
                if models.Students.objects.filter(email=form.get(studentEmail)).first():
                    # if they do, grab their user data to load into the new student account
                    student = models.Students(email = form.get(studentEmail),
                                              classname = models.Teachers.objects.get(id=receivingClass),
                                              first = models.Students.objects.filter(email=form.get(studentEmail)).first().first,
                                              last = models.Students.objects.filter(email=form.get(studentEmail)).first().last)
                    
            Websites = models.SearchingAlgorithm(input)


            print(Websites)

            models.DownloadWebsites(Websites)

            args = {'form': form, 'links': Websites}
            return render(request, 'DigitalBackpack/AssignmentWebpage.html', args)

        else:
            print("THIS IS ELSE")


            return render(request, 'DigitalBackpack/TeacherRegistration.html', {'form': form})

    else:
        # initialize our form
        form = TeacherRegistrationForm()
        return render(request, 'DigitalBackpack/TeacherRegistration.html', {'form': form})

# student registration view
#
# form for registering a new student account
def student_registration(request):
    # see if we've received a post input
    if request.method == 'POST':
        # if so, load the filled form
        form = TeacherRegistrationForm(request.POST)

        # check if our form is valid
        if form.is_valid():
            # if so, load new info into our user database
        
            # grab our username
            uname = form.cleaned_data['username']

            # save our form and user to the authentication db
            form.save()

            # and finally add them to the student group
            studentGroup, created = Group.objects.get_or_create(name='Students')
            newUser = User.objects.get(username=uname)
            newUser.groups.add(studentGroup)
            studentGroup.user_set.add(newUser)
            
            # authenticate user
            user_login = authenticate(username=form.cleaned_data['username'],
                                      password=form.cleaned_data['password1'],)
            login(request, user_login)

            # redirect to final registration
            return redirect('student_account_completion')

        else:
            # otherwise, kick the form back
            return render(request, 'DigitalBackpack/StudentRegistration.html', {'form': form})

    else:
        # otherwise, initialize our form
        form = StudentRegistrationForm()

        # render our form
        return render(request, 'DigitalBackpack/StudentRegistration.html', {'form': form})

# add assignment view
#
# view for the teacher's assignment addition form
@group_required('Teachers')
def new_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, teacher=User.objects.get(id=request.session.get('_auth_user_id')).username)
        
        if 'keywords' in request.POST:
            keywords = request.POST.get('keywords', '')
            resources = models.SearchingAlgorithm(keywords)

            return render(request, 'DigitalBackpack/NewAssignment.html', {'form': form, 'resources': resources })

    else:
        form = AssignmentForm(None, teacher=User.objects.get(id=request.session.get('_auth_user_id')).username)
    return render(request, 'DigitalBackpack/NewAssignment.html', {'form': form})

@group_required('Teachers')
def submit_new_assignment(request):
    if request.method == 'POST':
        print(request.POST)
        # build a form based off of the provided students to add
        form = AssignmentForm(request.POST, teacher=User.objects.get(id=request.session.get('_auth_user_id')).username)

        # ensure form is valid
        if form.is_valid():
            # if it is, create our new assignment

            # grab our form's cleaned data
            form = form.cleaned_data

            # pop off our class for use, as well as our number of arguments
            receivingClass = form.pop('classChoice')
            newTitle = form.pop('assignmentTitle')
            newDueDate = form.pop('assignmentDueDate')
            newInstructions = form.pop('assignmentInstructions')
            if(form.get('assignmentAttachment')):
                newAttachment = form.pop('assignmentAttachment', None)

                # if there is, load everything in with the attachment
                assignment = models.Assignments(title = newTitle,
                                                dueDate = newDueDate,
                                                classname = models.Teachers.objects.get(id=receivingClass),
                                                instructions = newInstructions,
                                                attachment = newAttachment)

            else:
                # otherwise, make one without
                assignment = models.Assignments(title = newTitle,
                                                dueDate = newDueDate,
                                                classname = models.Teachers.objects.get(id=receivingClass),
                                                instructions = newInstructions)

            # regardless of how we initialize, save our changes
            assignment.save()

            # now we move on to creating our resources
            
            # grab the assignment ID
            assignmentID = assignment.id
            
            # see if the teacher fetched resources
            try:
                resources = request.POST.getlist('resources')
                models.DownloadWebsites(resources, str(assignmentID))

            except KeyError as error:
                print("Teacher opted for no resources")

            # print success
            print("successfully created assignment")

            # redirect back to teacher page
            return redirect('teacher_page')

        else:
            # if something goes wrong, kick back to the new assignment page
            return redirect('new_assignment')

    else:
        return redirect('new_assignment')

# ratings view
#
# view for the website rating system.
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
