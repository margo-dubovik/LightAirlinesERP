from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login
from .forms import PassengerSignUpForm
from django.http import HttpResponse


def passenger_signup(request):
    if request.method == 'POST':
        form = PassengerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            login(request, user)
            return HttpResponse("registered successfully!")
            # return redirect('/account/login')
        return render(request, 'account/passenger_reg_form.html', {'form': form})

    else:
        form = PassengerSignUpForm()
        return render(request, 'account/passenger_reg_form.html', {'form': form})
