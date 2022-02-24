from django.shortcuts import render
from django.http import HttpResponse

def studentpage(request):
    return render(request, 'DigitalBackpack/StudentWebpage.html')

def teacherpage(request):
    return render(request, 'DigitalBackpack/TeacherWebpage.html')


