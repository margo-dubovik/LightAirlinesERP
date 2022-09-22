from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import PassengerProfile, StaffProfile


class PassengerSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address')
    first_name = forms.CharField(max_length=150, required=True, help_text='Required')
    last_name = forms.CharField(max_length=150, required=True, help_text='Required')

    class Meta:
        model = get_user_model()
        fields = (
            'email', 'first_name', 'last_name', 'password1', 'password2'
        )

    def save(self, commit=True):
        user = super(PassengerSignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
