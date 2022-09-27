from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ticket_search, name="ticket-search"),
    path('tickets/', views.tickets_form, name='tickets-form'),
    path('profile/', views.profile, name='profile'),
    path('profile/flights/upcoming', views.profile_upcoming_flights, name='upcoming-flights'),
    path('profile/flights/previous', views.profile_previous_flights, name='previous-flights'),
    path('profile/checkin', views.profile_online_check_in, name='online-checkin'),
    # path('airport_autocomplete', views.AirportAutocomplete.as_view(), name='airport-autocomplete',),
]
