from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
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
import DigitalBackpack.utils as utils
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login


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
    return render(request, 'DigitalBackpack/landingpage.html')

# login reroute view
#
# invisible view by which the system can check group permissions to decide where a user will be
# routed upon login
def login_reroute(request):
    try:
        if str(User.objects.get(id=request.session.get('_auth_user_id')).groups.first()) == "Teachers":
            request.session['currentClass'] = models.Teachers.objects.filter(user=User.objects.get(id=request.session.get('_auth_user_id'))).first().id
            return redirect('teacher_page')

        else:
            request.session['currentClass'] = models.Students.objects.filter(user=User.objects.get(id=request.session.get('_auth_user_id'))).first().id
            return redirect('student_page')

    except User.DoesNotExist:
        return redirect('landing_page')

# student view page
#
# records time student logs onto page and updates .csv
# returns student homepage
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

    return render(request, 'DigitalBackpack/studentpage.html')

# teacher view page
#
# returns teacher homepage
@group_required('Teachers')
def teacher_page(request):
    # fetch our class and student info
    classes = models.Teachers.objects.filter(user=User.objects.get(id=request.session.get('_auth_user_id'))).all()
    currentClassID = request.session['currentClass']
    students = models.Students.objects.filter(classname=models.Teachers.objects.get(id=currentClassID)).all()
    assignments = models.Assignments.objects.filter(classname=models.Teachers.objects.get(id=currentClassID)).all()
    print(classes)
    print(currentClassID)
    print(students)
    print(assignments)
    # render our request with this info
    return render(request, 'DigitalBackpack/teacherpage.html', {'classes': classes, 'students': students, 'currentClass': currentClassID, 'assignments': assignments})

# class registration page
#
# form allowing teachers to create new classes under their account
@group_required('Teachers')
def class_registration(request):
    # if we've received input for loading into the db
    if request.method == 'POST':
        # call our model submission
        form = ClassRegistrationForm(request.POST, request.POST)

        # ensure form is valid
        if form.is_valid():

            # grab our cleaned data
            data = form.cleaned_data

            # pass our cleaned date to the model for database interacton
            teacher = models.Teachers(user = User.objects.filter(username=data['username']).first(),
                                      first = data['first'],
                                      last = data['last'],
                                      classname = data['classname'])

            # save this information to the database
            teacher.save()

            # reset our session variable focus to this class
            request.session['currentClass'] = teacher.id

            # indicate success
            print("Successfully created class " + data['classname'] + ", taught by " + User.objects.filter(username=data['username']).first().username)

        else:
            # otherwise, kick back the form
            return render(request, 'DigitalBackpack/classregistration.html', {'form': form})

        # redirect our teacher to add students to this class
        return redirect('add_students')

    else:
        # pass our session to the form
        form = ClassRegistrationForm(None, username=request.session)

        # render our form
        return render(request, 'DigitalBackpack/classregistration.html', {'form': form})

# student account completion view
#
# grab additional user info from students to complete their account
@group_required('Students')
def student_account_completion(request):
    # if we've received input for updating the db
    if request.method == 'POST':
        # call our form creation
        form = StudentAccountCompletionForm(request.POST, request.POST)

        # ensure form is valid
        if form.is_valid():
            # grab our cleaned data
            data = form.cleaned_data

            # update our first name
            models.Students.objects.filter(email=User.objects.get(id=request.session.get('_auth_user_id')).email).update(first=data.get('first'))
            models.Students.objects.filter(email=User.objects.get(id=request.session.get('_auth_user_id')).email).update(last=data.get('last'))
            models.Students.objects.filter(email=User.objects.get(id=request.session.get('_auth_user_id')).email).update(user=User.objects.get(username=data.get('username')))

            # redirect our student to the homepage
            return redirect('student_page')

        else:
            # otherwise, kick back the form
            return render(request, 'DigitalBackpack/studentaccountcompletion.html', {'form': form})

    else:
        # pass our session info to the form
        form = StudentAccountCompletionForm(None, username=request.session)

        # render page
        return render(request, 'DigitalBackpack/studentaccountcompletion.html', {'form': form})

# add students form view
#
# form allowing teachers to add students to any of the classes associated with their account
@group_required('Teachers')
def add_students(request):
    if request.method == 'POST':
        form = AddStudentForm(request.POST, extra=request.POST.get('extraFieldCount'), teacher=User.objects.get(id=request.session.get('_auth_user_id')).username)
    else:
        form = AddStudentForm(None, teacher=User.objects.get(id=request.session.get('_auth_user_id')).username)
    return render(request, 'DigitalBackpack/addstudents.html', {'form': form})

# submit student additions view
#
# additional redirect to add_students view to allow for dynamic form allocation when not submitting
# NOTE: invisible view, will not present anything to user before redirect
@group_required('Teachers')
def submit_student_addition(request):
    if request.method == 'POST':
        # build a form based off of the provided students to add
        form = AddStudentForm(request.POST, extra=request.POST.get('extraFieldCount'), teacher=User.objects.get(id=request.session.get('_auth_user_id')).username)

        # ensure form is valid
        if form.is_valid():
            # if it is, load new students in

            # grab our form's cleaned data
            form = form.cleaned_data

            # pop off our class for use, as well as our number of arguments
            receivingClass = form.pop('classChoice')
            emailCount = form.pop('extraFieldCount')

            # loop through our remaining form items
            for studentEmail in form:
                # see if this user already has an account present
                if models.Students.objects.filter(email=form.get(studentEmail)).first():
                    # if they do, grab their user data to load into the new student account
                    student = models.Students(email = form.get(studentEmail),
                                              classname = models.Teachers.objects.get(id=receivingClass),
                                              first = models.Students.objects.filter(email=form.get(studentEmail)).first().first,
                                              last = models.Students.objects.filter(email=form.get(studentEmail)).first().last)

                else:
                    # otherwise, do the base initialization for the new student
                    student = models.Students(email = form.get(studentEmail),
                                              classname = models.Teachers.objects.get(id=receivingClass))

                # regardless of how we initialize, save our changes
                student.save()

                # indicate success to our additions
                print("Added student " + str(form.get(studentEmail) + " to " + str(receivingClass)))

            # redirect back to the homepage
            return redirect('teacher_page')

    # if anything goes wrong, kick back to the add students page
    return redirect('addstudents_page')

# teacher registration view
#
# form for registering a new teacher account
def teacher_registration(request):
    # see if we've received new class input
    if request.method == 'POST':
        print(request.POST)
        # if so, load the filled form
        form = TeacherRegistrationForm(request.POST)

        # check if our form is valid
        if form.is_valid():

            # if so, load new info into our user database

            # grab our user
            uname = form.cleaned_data['username']

            # save our form and user to the authentication db
            form.save()

            # and finally add them to the teacher group
            teacherGroup, created = Group.objects.get_or_create(name='Teachers')
            newUser = User.objects.get(username=uname)
            newUser.groups.add(teacherGroup)
            teacherGroup.user_set.add(newUser)

            # authenticate user
            user_login = authenticate(username=form.cleaned_data['username'],
                                      password=form.cleaned_data['password1'],)
            login(request, user_login)

            # redirect to class registration
            return redirect('class_registration')

        else:

            return render(request, 'DigitalBackpack/teacherregistration.html', {'form': form})

    else:
        # initialize our form
        form = TeacherRegistrationForm()
        return render(request, 'DigitalBackpack/teacherregistration.html', {'form': form})

# student registration view
#
# form for registering a new student account
def student_registration(request):
    # see if we've received a post input
    if request.method == 'POST':
        # if so, load the filled form
        form = StudentRegistrationForm(request.POST)

        # check if our form is valid
        if form.registeredEmail() and form.is_valid():
            # if so, load new info into our user database

            # grab our username
            uname = form.cleaned_data['username']
            studentEmail = form.cleaned_data['email']

            if models.Students.objects.filter(email=studentEmail):
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
                # otherwise, no email registered with the class
                return render(request, 'DigitalBackpack/studentregistration.html', {'form': form})

        else:
            # otherwise, kick the form back
            return render(request, 'DigitalBackpack/studentregistration.html', {'form': form})

    else:
        # otherwise, initialize our form
        form = StudentRegistrationForm()

        # render our form
        return render(request, 'DigitalBackpack/studentregistration.html', {'form': form})

# add assignment view
#
# view for the teacher's assignment addition form
@group_required('Teachers')
def new_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, teacher=User.objects.get(id=request.session.get('_auth_user_id')).username)

        if 'keywords' in request.POST:
            keywords = request.POST.get('keywords', '')
            resources = utils.searchingAlgorithm(keywords)

            return render(request, 'DigitalBackpack/newassignment.html', {'form': form, 'resources': resources })

    else:
        form = AssignmentForm(None, teacher=User.objects.get(id=request.session.get('_auth_user_id')).username)
    return render(request, 'DigitalBackpack/newassignment.html', {'form': form})

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
                utils.downloadWebsites(resources, str(assignmentID))

            except KeyError as error:
                print("Teacher opted for no resources")

            # print success
            print("successfully created assignment")

            # redirect back to teacher page
            return redirect('teacher_page')

        else:
            # if something goes wrong, kick back to the new assignment page
            return redirect('newassignment_page')

    else:
        return redirect('newassignment_page')

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
        return render(request, 'DigitalBackpack/ratings.html', {'form': form})

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

@group_required('Teachers')
def view_students(request):

    #This grabs the studentID that was sent from the button press in the Teacher Webpage
    #currentStudentID = request.session['studentID']
    currentStudentID = 1 # CHANGE (for testing purposes)

    #This checks to see if the currentStudentID is larger than the total number of students in model.py object.
    if(currentStudentID > models.Students.objects.count() or currentStudentID < 1):
        #If the student does not exist in the teacher's class list, then the student object will be set to None
        student = None

        #This sents the location of the studentOnlineConnectivityPath to None since
        #the student does not exist in the Database
        studentOnlineConnectivityPath = None

    #If the student is in their class list, this will set the object models.Students into one variable that can call its
    #other instances inside the models.students
    else:
        #This sents the student from the student database at the currentStudentID
        student = models.Students.objects.get(id = currentStudentID)

        #This is the location of the personal student's heatmap that is needed for
        #the viewstudent webpage.
        studentOnlineConnectivityPath = 'Users/Students/student_' + str(currentStudentID) + '/student_' + str(currentStudentID) + '_heatmap.png'

    #This prints the location as a test to see if the location is correct within
    #the terminal
    print(studentOnlineConnectivityPath)

    #This checks if the method on the request is POST. It also checks to see if
    #inside the POST request has the 'flagStudent' parameter. If so then enter
    #this if block statement. If there is there is no 'POST' in the request and
    #'flagStudent' is not in the POST request, then skip this if block statement
    if(request.method == 'POST' and 'flagStudent' in request.POST):
        #If so, the system will check if the student is currently flagged or not.
        #If the student is not flagged when the button is clicked.
        if(student.flagged == False):
            #Update the flagged instance as True.
            student.flagged = True
            #Save the changes made into the student Database
            student.save()
            #Redirect the viewer to the same page. This redirect's purpose is
            #to remove the "flagStudent" in the POST. This also prevents the
            #form to make a pop up asking to use the information to carry over
            #on the refresh of the page.
            return redirect('view_student')

        #If the student is already flagged.
        else:
            #Update the flagged instance as False
            student.flagged = False
            #Save the changes made into the student Database
            student.save()
            #Redirect the viewer to the same page. This redirect's purpose is
            #to remove the "flagStudent" in the POST. This also prevents the
            #form to make a pop up asking to use the information to carry over
            #on the refresh of the page.
            return redirect('view_student')


    #Once that is done, render the page again to update the page with the latest
    #information that was changed. The render sends the student's information,
    #the session ID that was sent in, and the location of the online connectivity
    #heatmap.
    return render(request, 'DigitalBackpack/TeacherViewStudent.html',
                  {
                      "studentID": currentStudentID,
                      "student": student,
                      "onlineconnectivity": studentOnlineConnectivityPath,
                  })
