from django.urls import path, include
from . import views

urlpatterns = [
    path('passenger/activate/<uidb64>/<token>', views.activate_passenger, name="activate-passenger"),
    path('passenger/signup/', views.passenger_signup, name="passenger-signup"),
    path('passenger/login/', views.passenger_login, name="passenger-login"),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('staff/login/', views.staff_login, name="staff-login"),
    path('logout/', views.user_logout, name="logout"),
]