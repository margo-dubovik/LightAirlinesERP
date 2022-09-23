from django import forms
from django.contrib.auth import get_user_model
from dal import autocomplete

from airline.models import FareClass, BaggagePrice, Airplane, Airport, Flight, Booking, Ticket, Discount


class FlightSearchForm(forms.Form):
    origin = forms.CharField(required=True, max_length=150, label="From")
    destination = forms.CharField(required=True, max_length=150, label="To")
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                           help_text="if no specific date, leave blank", required=False)
    n_passengers = forms.IntegerField(initial=1, label="Number of passengers")
    fare_class = forms.ChoiceField(choices=((3, "Economy"), (2, "Business",), (1, "First"),), initial="Economy")

    class Meta:
        widgets = {
            'origin': autocomplete.ListSelect2(url='airport-autocomplete'),
            'destination': autocomplete.ListSelect2(url='airport-autocomplete'),
        }