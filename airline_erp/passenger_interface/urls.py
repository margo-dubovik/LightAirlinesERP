from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_view, name="home-view"),
    path('account/', include('account.urls')),
    path('ticket-search-result', views.ticket_search_result, name='ticket-search-result')
    # path('airport_autocomplete', views.AirportAutocomplete.as_view(), name='airport-autocomplete',),
]