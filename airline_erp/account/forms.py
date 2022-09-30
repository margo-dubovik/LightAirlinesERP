from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

from .models import PassengerProfile, StaffProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address')
    first_name = forms.CharField(max_length=150, required=True, help_text='Required')
    last_name = forms.CharField(max_length=150, required=True, help_text='Required')

    class Meta:
        model = get_user_model()
        fields = (
            'email', 'first_name', 'last_name', 'password1', 'password2'
        )

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


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


class UserCreationAdminForm(CustomUserCreationForm):

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_airline_staff = self.cleaned_data['is_airline_staff']
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', )


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
