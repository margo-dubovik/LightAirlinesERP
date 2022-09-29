from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from dal import autocomplete
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from airline.models import FareClass, ComfortsPrice, Airplane, Airport, Flight, Booking, Ticket, Discount
from account.forms import CustomUserCreationForm
from account.models import StaffProfile
# from .widgets import DateTimePickerInput


class TicketCodeForm(forms.Form):
    ticket_code = forms.IntegerField(label="Ticket Code")


class BagForm(forms.Form):
    additional_bags = forms.IntegerField(label="Number of additional bags")


class ManagerProfileCreationForm(forms.Form):
    role_choices = (
        ('gate_manager', 'Gate Manager'),
        ('checkin_manager', 'Check-in manager'),
    )

    airport = forms.ModelMultipleChoiceField(queryset=Airport.objects.all(), required=True)
    role = forms.ChoiceField(choices=role_choices, required=True)

    prefix = 'manager_profile'

    class Meta:
        model = StaffProfile
        fields = (
            'role', 'airport',
        )


class ManagerSearchForm(forms.Form):
    manager_first_name = forms.CharField(max_length=150, required=True)
    manager_last_name = forms.CharField(max_length=150, required=True)


class AddFlightForm(ModelForm):

    class Meta:
        model = Flight
        exclude = ('is_cancelled', )
        widgets = {
            'departure_time': DateTimePickerInput(),
        }


class StaffFlightSearchForm(ModelForm):
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                           help_text="if no specific date, leave blank", required=False)

    class Meta:
        model = Flight
        fields = (
            'origin', 'destination',
        )