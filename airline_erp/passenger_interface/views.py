from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from django.core.cache import cache

from .forms import FlightSearchForm
from airline.models import FareClass, BaggagePrice, Airplane, Airport, Flight, Booking, Ticket, Discount

from dal import autocomplete

#
# class AirportAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         qs = Airport.objects.all()
#         print("IM IN A VIEW")
#         if self.q:
#             qs = qs.filter(Q(name__istartswith=self.q) | Q(city__istartswith=self.q))
#
#         return qs


def ticket_search(request):
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
            if results:
                print("results=", results, "type=", type(results))
            else:
                print("NO RESULTS")
            return render(request, "passenger_interface/ticket_search.html",
                          {'form': form, 'results': results, 'form_data': cd, })
        else:
            return render(request, "passenger_interface/ticket_search.html", {'form': form})
    else:
        form = FlightSearchForm()
        return render(request, "passenger_interface/ticket_search.html", {'form': form, 'initial': True})


def tickets_form(request):
    if request.method == 'POST':
        pass
    else:
        n_passengers = request.GET.get('n_passengers')
        flight_id = request.GET.get('flight_id')
        return HttpResponse(f'Let`s order {n_passengers} tickets for flight={flight_id}!')
