from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ticket_search, name="ticket-search"),
    path('tickets/', views.tickets_form, name='tickets-form'),
    path('profile/', views.profile, name='profile'),
    path('profile/bookings/upcoming', views.profile_upcoming_bookings, name='upcoming-bookings'),
    path('profile/bookings/upcoming/<int:booking_id>', views.booking_details_view, name='booking-details'),
    path('profile/bookings/previous', views.profile_previous_bookings, name='previous-bookings'),
]
