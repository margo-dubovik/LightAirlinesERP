from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/', views.staff_profile_redirect, name="staff-profile-redirect"),
    path('profile/gate-manager/<int:id>', views.GateManagerProfile.as_view(), name="gate-manager-profile"),
    path('register-boarding/', views.register_boarding, name="register-boarding"),
    path('profile/checkin-manager/<int:id>', views.CheckinManagerProfile.as_view(), name="checkin-manager-profile"),
    path('checkin/', views.checkin_passenger, name="checkin"),
    path('checkin-options/', views.checkin_add_options, name="checkin-options"),
    path('profile/supervisor/<int:id>', views.SupervisorProfile.as_view(), name="supervisor-profile"),
    path('supervisor/managers-actions', views.ManagersActions.as_view(), name="managers-actions"),
    path('supervisor/managers-list', views.managers_list, name="managers-list"),
    path('supervisor/add-manager', views.add_manager, name="add-manager"),
    path('supervisor/remove-manager', views.remove_manager, name="remove-manager"),
    path('supervisor/flights-actions', views.flights_actions, name="flights-actions"),
    path('supervisor/add-flight', views.add_flight, name="add-flight"),
    path('supervisor/cancel-flight', views.cancel_flight, name="cancel-flight"),
]