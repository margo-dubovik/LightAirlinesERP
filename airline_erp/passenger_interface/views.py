import decimal

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from django.core.cache import cache
from django.forms import formset_factory
from django.utils import timezone

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
    price_fields = {
        1: flight.first_class_price,
        2: flight.business_class_price,
        3: flight.economy_class_price,
    }

    ticket_price = price_fields[fare_class.pk]

    if Discount.objects.filter(flight=flight).exists():
        discount = Discount.objects.get(flight=flight)
        discount_fields = {
            1: discount.first_class_discount,
            2: discount.business_class_discount,
            3: discount.economy_class_discount,
        }
        return ticket_price * (1 - discount_fields[fare_class.pk] * decimal.Decimal(0.01))
    else:
        return ticket_price


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
    if ticket.lunch:
        prices = ComfortsPrice.objects.get(fare_class=ticket.fare_class)
        return prices.lunch_price
    else:
        return 0


def update_flight_seats(flight):
    classes = {
        'first': 1,
        'business': 2,
        'economy': 3,
    }
    first_class = get_object_or_404(FareClass, pk=classes['first'])
    business_class = get_object_or_404(FareClass, pk=classes['business'])
    economy_class = get_object_or_404(FareClass, pk=classes['economy'])
    first_seats = 0
    business_seats = 0
    economy_seats = 0
    for booking in flight.bookings.all():
        first_seats += booking.tickets.filter(fare_class=first_class).count()
        business_seats += booking.tickets.filter(fare_class=business_class).count()
        economy_seats += booking.tickets.filter(fare_class=economy_class).count()
    flight.first_class_seats_occupied = first_seats
    flight.business_class_seats_occupied = business_seats
    flight.economy_class_seats_occupied = economy_seats
    flight.save()


def ticket_search(request):
    if request.method == 'POST':
        form = FlightSearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['date']:
                results = Flight.objects.filter(
                    Q(origin__city__icontains=cd['origin'], destination__city__icontains=cd['destination'],
                      departure_time__icontains=cd['date'], )
                )
            else:
                results = Flight.objects.filter(
                    Q(origin__city__icontains=cd['origin'], destination__city__icontains=cd['destination'])
                )
            if results:
                for flight in results:
                    fare_class = cd['fare_class']
                    n_passengers = cd['n_passengers']
                    available_seats = {
                        '1': flight.first_class_seats_available,
                        '2': flight.business_class_seats_available,
                        '3': flight.economy_class_seats_available,
                    }
                    if available_seats[fare_class] < n_passengers:
                        results = results.exclude(pk=flight.pk)
            return render(request, "passenger_interface/ticket_search.html",
                          {'form': form, 'results': results, 'form_data': cd, })
        else:
            return render(request, "passenger_interface/ticket_search.html", {'form': form})
    else:
        form = FlightSearchForm()
        return render(request, "passenger_interface/ticket_search.html", {'form': form, 'initial': True})


@login_required
def tickets_form(request):
    n_passengers = int(request.GET.get('n_passengers'))
    TicketsFormset = formset_factory(TicketForm, extra=n_passengers)
    flight_id = request.GET.get('flight_id')
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == 'POST':
        formset = TicketsFormset(request.POST or None)
        if formset.is_valid():
            booking = Booking(flight=flight, purchaser=request.user.passenger_profile)
            booking.save()
            total_booking_price = 0
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
                total_booking_price += ticket.total_price
                # occupy_seat(flight, ticket.fare_class)
            booking.total_price = total_booking_price
            booking.save()
            update_flight_seats(flight)  # add just taken seats
            return HttpResponse("Oder taken!")
        else:
            messages.error(request, f"Formset errors: {formset.errors}")
            messages.error(request, f"Formset non-form errors: {formset.non_form_errors()}")
        return render(request, 'passenger_interface/tickets_form.html',
                      {'formset': TicketsFormset, 'flight': flight, })
    else:
        return render(request, 'passenger_interface/tickets_form.html',
                      {'formset': TicketsFormset, 'flight': flight, })


@login_required
def profile(request):
    return render(request, 'passenger_interface/profile_profile.html')


@login_required
def profile_upcoming_bookings(request):
    upcoming_bookings = request.user.passenger_profile.bookings.filter(flight__departure_time__gt=timezone.now())
    print("upcoming_bookings=", upcoming_bookings)
    return render(request, 'passenger_interface/profile_upcoming_bookings.html', {'bookings': upcoming_bookings, })


@login_required
def profile_previous_bookings(request):
    previous_bookings = request.user.passenger_profile.bookings.filter(flight__departure_time__lt=timezone.now())
    print("previous_bookings=", previous_bookings)
    return render(request, 'passenger_interface/profile_previous_bookings.html', {'bookings': previous_bookings, })


@login_required
def profile_online_check_in(request):
    return render(request, 'passenger_interface/profile_online_check_in.html')
