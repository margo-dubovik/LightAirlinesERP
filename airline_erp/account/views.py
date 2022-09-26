from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.contrib import messages

from .forms import PassengerSignUpForm, LoginForm
from .models import PassengerProfile, StaffProfile


def passenger_signup(request):
    if request.method == 'POST':
        form = PassengerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            passenger_profile = PassengerProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Signed up successfully')
            redirect(reverse('ticket-search'))
        return render(request, 'account/passenger_reg_form.html', {'form': form})

    else:
        form = PassengerSignUpForm()
        return render(request, 'account/passenger_reg_form.html', {'form': form})


def passenger_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    if not user.is_staff:
                        login(request, user)
                        messages.success(request, 'Logged in successfully')
                        next_param = request.GET.get('next')
                        if next_param:
                            url = next_param
                        else:
                            url = reverse('ticket-search')
                        return redirect(url)
                    else:
                        messages.error(request, 'This account is not a passenger! Please use "Staff Log In" ')
                        return redirect(reverse('staff-login'))
                else:
                    messages.error(request, 'The account is deactivated')
            else:
                messages.error(request, 'user not found')
        return render(request, 'account/login.html', {'form': form, 'login_title': 'Log In', })
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form, 'login_title': 'Log In', })


def staff_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    messages.success(request, 'Logged in successfully')
                    return redirect(reverse('ticket-search'))
                else:
                    messages.error(request, 'This account is not a staff member! Please use "Log In"')
                    return redirect(reverse('passenger-login'))
            else:
                messages.error(request, 'user not found')
        return render(request, 'account/login.html', {'form': form, 'login_title': 'Staff Log In', })
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form, 'login_title': 'Staff Log In', })


def user_logout(request):
    logout(request)
    messages.info(request, 'You are logged out now')
    return redirect(reverse('ticket-search'))
