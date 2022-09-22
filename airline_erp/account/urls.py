from django.urls import path
from . import views

urlpatterns = [
    path('passenger/signup/', views.passenger_signup, name="passenger-signup")
]