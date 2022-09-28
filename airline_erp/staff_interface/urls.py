from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/', views.staff_profile_redirect, name="staff-profile-redirect"),
    path('gate-manager/profile', views.gate_manager_profile, name="gate-manager-profile"),
]