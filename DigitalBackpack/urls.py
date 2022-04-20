from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path( '', views.landing_page, name='landing_page' ),
    path( 'register/teacher/', views.teacher_registration, name='teacher_registration' ),
    path( 'register/student/', views.student_registration, name='student_registration' ),
    path( 'register/complete-student', views.student_account_completion, name='student_account_completion' ),
    path( 'login/reroute/', views.login_reroute, name='login_reroute' ),
    path( 'login/teacher/', auth_views.LoginView.as_view(template_name='DigitalBackpack/teacherlogin.html'), name='teacher_login' ),
    path( 'login/student/', auth_views.LoginView.as_view(template_name='DigitalBackpack/studentlogin.html'), name='student_login' ),
    path( 'register/class/', views.class_registration, name='class_registration' ),
    path( 'logout/', auth_views.LogoutView.as_view(template_name='DigitalBackpack/logout.html'), name='logout' ),
    path( 'student/', views.student_page, name='student_page' ),
    path( 'teacher/', views.teacher_page, name='teacher_page' ),
    path( 'teacher/addstudents/', views.add_students, name='add_students' ),
    path( 'teacher/submitStudentAdditions/', views.submit_student_addition, name='submit_student_additions' ),
    path( 'teacher/newAssignment/', views.new_assignment, name='new_assignment' ),
    path( 'teacher/submitNewAssignment/', views.submit_new_assignment, name='submit_new_assignment' ),
    path( 'ratings/', views.ratings, name='ratings'),
    # path( 'student/viewmyself/', views.connection_page, name='connection_timeframe_page' ),
    path( 'teacher/viewstudent/', views.view_student, name='view_student' ),
    path( 'student/viewmyself/', views.view_myself, name='view_myself' ),
]
