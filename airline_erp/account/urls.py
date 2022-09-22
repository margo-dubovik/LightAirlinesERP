from django.urls import path
from . import views

urlpatterns = [
    path('passenger/signup/', views.passenger_signup, name="passenger-signup"),
    path('passenger/login/', views.passenger_login, name="passenger-login"),
    path('staff/login/', views.staff_login, name="staff-login"),
    path('logout/', views.user_logout, name="logout"),
]