from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # Homepage
    path('hostels/', views.hostels, name='hostels'),  # Hostels page
    path('login/', views.general_login, name='general_login'),  # General login selector
    path('choose-role/', views.choose_role, name='choose_role'),
    path('login/student/', views.student_login, name='student_login'),
    path('login/staff/', views.staff_login, name='staff_login'),  # Staff login
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
]
