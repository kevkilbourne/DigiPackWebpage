from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import sqlite3
import importlib
import DigitalBackpack.models as models

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
        # if they are sent via get to send ratings, give them the page
        return render(request, 'DigitalBackpack/Ratings.html')

