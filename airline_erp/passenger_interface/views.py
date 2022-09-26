from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from django.core.cache import cache
from django.forms import formset_factory

from .forms import FlightSearchForm, TicketForm
from airline.models import FareClass, ComfortsPrice, Airplane, Airport, Flight, Booking, Ticket, Discount

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


def get_fare_class_price(flight, fare_class):
    if fare_class.pk == 1:
        return flight.first_class_price
    elif fare_class.pk == 2:
        return flight.business_class_price
    elif fare_class.pk == 3:
        return flight.economy_class_price


def get_baggage_price(ticket):
    prices = ComfortsPrice.objects.get(fare_class=ticket.fare_class)
    if ticket.n_bags == 0:
        return 0
    elif ticket.n_bags == 1:
        return prices.first_bag_price
    elif ticket.n_bags == 2:
        return prices.first_bag_price + prices.second_bag_price
    else:
        return prices.three_or_more_bags_price


def get_lunch_price(ticket):
    prices = ComfortsPrice.objects.get(fare_class=ticket.fare_class)
    return prices.lunch_price


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
    n_passengers = int(request.GET.get('n_passengers'))
    TicketsFormset = formset_factory(TicketForm, extra=n_passengers)
    if request.method == 'POST':
        flight_id = request.GET.get('flight_id')
        flight = get_object_or_404(Flight, id=flight_id)
        formset = TicketsFormset(request.POST or None)
        if formset.is_valid():
            booking = Booking(flight=flight, purchaser=request.user.passenger_profile)
            print("FORMSET:")
            for form in formset:
                cd = form.cleaned_data
                ticket = form.save(commit=False)
                ticket.booking = booking
                ticket.fare_class = get_object_or_404(FareClass, pk=cd['fare_class'])
                ticket.baggage_price = get_baggage_price(ticket)
                fare_class_price = get_fare_class_price(flight, ticket.fare_class)
                lunch_price = get_lunch_price(ticket)
                ticket.total_price = fare_class_price + ticket.baggage_price + lunch_price
                ticket.save()
            return HttpResponse("Oder taken!")
        else:
            messages.error(request, f"Formset errors: {formset.errors}")
            messages.error(request, f"Formset non-form errors: {formset.non_form_errors()}")
        return render(request, 'passenger_interface/tickets_form.html',
                      {'formset': TicketsFormset, })
    else:
        return render(request, 'passenger_interface/tickets_form.html',
                      {'formset': TicketsFormset, })
