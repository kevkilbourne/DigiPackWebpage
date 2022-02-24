from django.urls import path
from . import views

urlpatterns = [
    path( 'student/', views.studentpage, name='student_page' ),
    path( 'teacher/', views.teacherpage, name='teacher_page' ),
]