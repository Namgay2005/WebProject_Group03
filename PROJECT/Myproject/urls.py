from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # Homepage
    path('hostels/', views.hostels, name='hostels'),  # Hostels page
    path('dechenling/', views.dechenling, name='dechenling'),  # Dechenling hostel
    path('login/', views.general_login, name='general_login'),  # General login selector
    path('choose-role/', views.choose_role, name='choose_role'),
    path('login/student/', views.student_login, name='student_login'),
    path('login/staff/', views.sso_login, name='staff_login'),  # For backward compatibility
    path('login/sso/', views.sso_login, name='sso_login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/logout/', views.student_logout, name='student_logout'),  # Student logout
    path('student/complaints/', views.student_complaints, name='student_complaints'),
    path('student/maintenance/', views.student_maintenance, name='student_maintenance'),
    path('student/leave/', views.student_leave, name='student_leave'),
    path('student/attendance/', views.student_attendance, name='student_attendance'),
    path('sso/dashboard/', views.sso_dashboard, name='sso_dashboard'),
    path('sso/logout/', views.sso_logout, name='sso_logout'),
    path('sso/complaints/', views.sso_complaints, name='sso_complaints'),
    path('sso/maintenance/', views.sso_maintenance, name='sso_maintenance'),
    path('sso/leave/', views.sso_leave, name='sso_leave'),
    path('sso/attendance/', views.sso_attendance, name='sso_attendance'),
]
