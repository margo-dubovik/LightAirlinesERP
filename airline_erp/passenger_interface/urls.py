from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ticket_search, name="ticket-search"),
    path('account/', include('account.urls')),
    path('tickets/', views.tickets_form, name='tickets-form'),
    # path('airport_autocomplete', views.AirportAutocomplete.as_view(), name='airport-autocomplete',),
]
