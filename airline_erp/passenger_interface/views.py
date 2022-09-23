from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q

from .forms import FlightSearchForm
from airline.models import FareClass, BaggagePrice, Airplane, Airport, Flight, Booking, Ticket, Discount


def home_view(request):
    if request.method == 'POST':
        form = FlightSearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            result = Flight.objects.filter(
                Q(origin__icontains=cd['origin'], destination__icontains=cd['destination'])
            )
            return redirect(reverse('home-view'))
        else:
            return render(request, "passenger_interface/passenger_interface_home.html", {'form': form})
    else:
        form = FlightSearchForm()
        return render(request, "passenger_interface/passenger_interface_home.html", {'form': form})

