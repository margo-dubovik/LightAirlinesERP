from django import forms
from django.contrib.auth import get_user_model

from airline.models import FareClass, BaggagePrice, Airplane, Airport, Flight, Booking, Ticket, Discount


class FlightSearchForm(forms.Form):
    origin = forms.CharField(required=True, max_length=150, label="from")
    destination = forms.CharField(required=True, max_length=150, label="to")
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                           help_text="if no specific date, leave blank", required=False)
    n_passengers = forms.IntegerField(initial=1, label="number of passengers")
    fare_class = forms.ChoiceField(choices=((3, "economy"), (2, "business",), (1, "first"),), initial="economy")
