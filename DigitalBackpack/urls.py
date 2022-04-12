from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path( '', views.landing_page, name='landing_page' ),
    path( 'register/teacher/', views.teacher_registration, name='teacher_registration' ),
    path( 'register/student/', views.student_registration, name='student_registration' ),
    path( 'register/complete-student', views.student_account_completion, name='student_account_completion' ),
    # path( 'login/reroute/', views.login_reroute, name='login_reroute' ),
    path( 'login/teacher/', auth_views.LoginView.as_view(template_name='DigitalBackpack/TeacherLogin.html'), name='teacher_login' ),
    path( 'login/student/', auth_views.LoginView.as_view(template_name='DigitalBackpack/StudentLogin.html'), name='student_login' ),
    path( 'register/class/', views.class_registration, name='class_registration' ),
    path( 'logout/', auth_views.LogoutView.as_view(template_name='DigitalBackpack/Logout.html'), name='logout' ),
    path( 'student/', views.student_page, name='student_page' ),
    path( 'teacher/', views.teacher_page, name='teacher_page' ),
    path( 'teacher/addstudents/', views.add_students, name='add_students' ),
    path( 'teacher/submitStudentAdditions/', views.submit_student_addition, name='submit_student_additions' ),
    path( 'teacher/newAssignment/', views.new_assignment, name='new_assignment' ),
    # path( 'teacher/submitNewAssignment/', views.submit_new_assignment, name='submit_new_assignment' ),
    path( 'ratings/', views.ratings, name='ratings'),
    path( 'student/connectivity/', views.connection_page, name='connection_timeframe_page' ),


    path( 'studentbs/', views.student_page_bs, name='student_bootstrap_page' ),
    path( 'teacherbs/', views.teacher_page_bs, name='teacher_bootstrap_page' ),
    path( 'landingbs/', views.landing_page_bs, name='landing_bootstrap_page' ),
    path( 'studentregistrationbs/', views.student_registration_bs, name='student_registration_page' ),
    path( 'teacherregistrationbs/', views.teacher_registration_bs, name='teacher_registration_page' ),
    path( 'studentloginbs/', auth_views.LoginView.as_view(template_name='DigitalBackpack/bs/studentlogin_bs.html'), name='student_login_page' ),
    path( 'teacherloginbs/', auth_views.LoginView.as_view(template_name='DigitalBackpack/bs/teacherlogin_bs.html'), name='teacher_login_page' ),
    path( 'classregistrationbs/', views.class_registration_bs, name='class_registration_page' ),
    path( 'logoutbs/', views.logout_bs, name='logout_page' ),
    path( 'ratingsbs/', views.ratings_bs, name='ratings_page' ),
    path( 'newassignmentbs/', views.new_assignment_bs, name='newassignment_page' ),
    path( 'addstudentsbs/', views.add_students_bs, name='addstudents_page' ),
    path( 'studentaccountcompletionbs/', views.student_account_completion_bs, name='student_account_completion_page' ),
    path( 'viewstudentbs/', views.view_student_bs, name='view_student_page' ),
    path( 'submitstudentadditionsbs/', views.submit_student_addition_bs, name='submit_student_additions_bs' ),
    path( 'login/reroute/', views.login_reroute_bs, name='login_reroute_bs' ),

    path( 'teacher/submitNewAssignment/', views.submit_new_assignment_bs, name='submit_new_assignment_page' ),
]
