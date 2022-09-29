from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/', views.staff_profile_redirect, name="staff-profile-redirect"),
    path('profile/gate-manager/', views.gate_manager_profile, name="gate-manager-profile"),
    path('register-boarding/', views.register_boarding, name="register-boarding"),
    path('profile/checkin-manager/', views.checkin_manager_profile, name="checkin-manager-profile"),
    path('checkin/', views.checkin_passenger, name="checkin"),
    path('checkin-options/', views.checkin_add_options, name="checkin-options"),
    path('profile/supervisor/', views.supervisor_profile, name="supervisor-profile"),
    path('supervisor/managers-actions', views.managers_actions, name="managers-actions"),
    path('supervisor/add-manager', views.add_manager, name="add-manager"),
]