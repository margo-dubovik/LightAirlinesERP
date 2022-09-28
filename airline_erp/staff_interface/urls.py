from django.urls import path, include
from . import views

urlpatterns = [
    path('staff/gate-manager/profile', views.gate_manager_profile, name="gate-manager-profile"),
]