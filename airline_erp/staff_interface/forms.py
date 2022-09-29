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


class StaffUserCreationForm(CustomUserCreationForm):

    prefix = 'staff_user'

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_airline_staff = True
        if commit:
            user.save()
        return user


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


