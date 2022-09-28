from django import forms
from django.contrib.auth import get_user_model
from dal import autocomplete

from airline.models import FareClass, ComfortsPrice, Airplane, Airport, Flight, Booking, Ticket, Discount


class TicketCodeForm(forms.Form):
    ticket_code = forms.IntegerField(label="Ticket Code")
