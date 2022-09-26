from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from django.core.cache import cache

from .forms import FlightSearchForm
from airline.models import FareClass, BaggagePrice, Airplane, Airport, Flight, Booking, Ticket, Discount

from dal import autocomplete


class AirportAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Airport.objects.all()
        print("IM IN A VIEW")
        if self.q:
            qs = qs.filter(Q(name__istartswith=self.q) | Q(city__istartswith=self.q))

        return qs


def home_view(request):
    if request.method == 'POST':
        form = FlightSearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['date']:
                results = Flight.objects.filter(
                    Q(origin__city__icontains=cd['origin'], destination__city__icontains=cd['destination'],
                      departure_time__icontains=cd['date'])
                )
            else:
                results = Flight.objects.filter(
                    Q(origin__city__icontains=cd['origin'], destination__city__icontains=cd['destination'])
                )
            print("results=", results)
            cache.set('ticket_search_results', results, 10)
            return redirect(reverse('ticket-search-result'))
        else:
            return render(request, "passenger_interface/passenger_interface_home.html", {'form': form})
    else:
        form = FlightSearchForm()
        return render(request, "passenger_interface/passenger_interface_home.html", {'form': form})


def ticket_search_result(request):
    results = cache.get('ticket_search_results')
    return render(request, "passenger_interface/flights_found.html", {'results': results})
