from django import forms
from django.contrib.auth import get_user_model

from airline.models import FareClass, ComfortsPrice, Airplane, Airport, Flight, Booking, Ticket, Discount
from django.forms import ModelForm


class FlightSearchForm(ModelForm):
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                           help_text="if no specific date, leave blank", required=False)
    n_passengers = forms.IntegerField(initial=1, label="Number of passengers")
    fare_class = forms.ChoiceField(choices=((3, "Economy"), (2, "Business",), (1, "First"),), initial="Economy")

    class Meta:
        model = Flight
        fields = (
            'origin', 'destination',
        )


class TicketForm(forms.ModelForm):
    passenger_first_name = forms.CharField(max_length=150)
    passenger_last_name = forms.CharField(max_length=150)
    fare_class = forms.ChoiceField(choices=((3, "Economy"), (2, "Business",), (1, "First"),), initial="Economy")
    n_bags = forms.IntegerField(label="Number of bags")
    lunch = forms.BooleanField(required=False)

    class Meta:
        model = Ticket
        fields = (
            'passenger_first_name', 'passenger_last_name', 'n_bags', 'lunch'
        )

    def save(self, commit=True):
        ticket = super(TicketForm, self).save(commit=False)
        ticket.passenger_first_name = self.cleaned_data['passenger_first_name']
        ticket.passenger_last_name = self.cleaned_data['passenger_last_name']
        ticket.n_bags = self.cleaned_data['n_bags']
        ticket.lunch = self.cleaned_data['lunch']
        if commit:
            ticket.save()
        return ticket
