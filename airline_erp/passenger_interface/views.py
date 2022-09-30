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
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .forms import FlightSearchForm, TicketForm
from airline.models import FareClass, ComfortsPrice, Airplane, Airport, Flight, Booking, Ticket, Discount


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
        return round(ticket_price * (1 - discount_fields[fare_class.pk] * decimal.Decimal(0.01)), 2)
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


def send_email(request, booking):
    email_subject = "Your LightAirlines tickets"
    email_body = render_to_string('passenger_interface/tickets_template.html',
                                  {'user': request.user,
                                   'tickets': booking.tickets.all(),
                                   'flight': booking.flight,
                                   'email': True, },
                                  request=request,
                                  )

    send_mail(
        subject=email_subject,
        message=" ",
        html_message=email_body,
        from_email=settings.EMAIL_FROM_USER,
        recipient_list=[request.user.email],
        fail_silently=True,
    )


def ticket_price_calculate(flight, fare_class, lunch, n_bags,):
    total_price = 0
    fare_class_price = get_fare_class_price(flight, fare_class)
    comforts_prices = ComfortsPrice.objects.get(fare_class=fare_class)
    if lunch:
        total_price += comforts_prices.lunch_price
    if n_bags == 0:
        bags_price = 0
    elif n_bags == 1:
        bags_price = comforts_prices.first_bag_price
    elif n_bags == 2:
        bags_price = comforts_prices.first_bag_price + comforts_prices.second_bag_price
    else:
        bags_price = comforts_prices.three_or_more_bags_price

    total_price += fare_class_price + bags_price
    return total_price


def ticket_search(request):
    if request.method == 'POST':
        form = FlightSearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['date']:
                results = Flight.objects.filter(
                    Q(origin=cd['origin'], destination=cd['destination'],
                      departure_time__icontains=cd['date'], departure_time__gt=timezone.now(), is_cancelled=False, )
                )
            else:
                results = Flight.objects.filter(
                    Q(origin=cd['origin'], destination=cd['destination'],
                      departure_time__gt=timezone.now(), is_cancelled=False, )
                )
            if results:
                for flight in results:
                    fare_class_pk = cd['fare_class']
                    n_passengers = cd['n_passengers']
                    available_seats = {
                        '1': flight.first_class_seats_available,
                        '2': flight.business_class_seats_available,
                        '3': flight.economy_class_seats_available,
                    }
                    if available_seats[fare_class_pk] < n_passengers:
                        results = results.exclude(pk=flight.pk)

                    else:
                        fare_class = FareClass.objects.get(pk=fare_class_pk)
                        fare_class_price = get_fare_class_price(flight, fare_class)
                        try:
                            discount = Discount.objects.get(flight=flight)
                            discount_fields = {
                                '1': discount.first_class_discount,
                                '2': discount.business_class_discount,
                                '3': discount.economy_class_discount,
                            }
                            discount_percent = discount_fields[fare_class_pk]
                        except Discount.DoesNotExist:
                            discount_percent = None

                        booking_price = round(fare_class_price * n_passengers, 2)

            return render(request, "passenger_interface/ticket_search.html",
                          {'form': form, 'results': results, 'form_data': cd,
                           'n_passengers': n_passengers, 'booking_price': booking_price,
                           'discount_percent': discount_percent, 'fare_class_pk': fare_class_pk})
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
    fare_class_id = int(request.GET.get('fare_class'))
    fare_class = FareClass.objects.get(pk=fare_class_id)
    flight = get_object_or_404(Flight, id=flight_id)
    one_ticket_price = round(get_fare_class_price(flight, fare_class), 2)
    comforts_prices = ComfortsPrice.objects.get(fare_class=fare_class)
    if request.method == 'POST':
        formset = TicketsFormset(request.POST or None)
        if formset.is_valid():
            confirmed = request.POST.get('confirmed')
            print("confirmed=", confirmed)
            if confirmed:  # if passenger confirmed order
                booking = Booking(flight=flight, purchaser=request.user.passenger_profile)
                booking.save()
                total_booking_price = 0
                for form in formset:
                    cd = form.cleaned_data
                    ticket = form.save(commit=False)
                    ticket.booking = booking
                    ticket.fare_class = fare_class
                    ticket.baggage_price = get_baggage_price(ticket)
                    fare_class_price = get_fare_class_price(flight, ticket.fare_class)
                    lunch_price = get_lunch_price(ticket)
                    ticket.total_price = fare_class_price + ticket.baggage_price + lunch_price
                    ticket.save()
                    total_booking_price += ticket.total_price
                booking.total_price = total_booking_price
                booking.save()
                update_flight_seats(flight)  # add just taken seats

                send_email(request, booking)

                messages.success(request, f"Tickets booked successfully! They were sent to your email."
                                          f"You can also find them in your profile")
                return redirect(reverse('upcoming-bookings'))

            else:  # calculate booking price
                total_booking_price = 0
                for form in formset:
                    cd = form.cleaned_data
                    lunch = cd['lunch']
                    n_bags = cd['n_bags']
                    ticket_price = ticket_price_calculate(flight, fare_class, lunch, n_bags)
                    total_booking_price += ticket_price
                total_booking_price = round(total_booking_price, 2)
                return render(request, 'passenger_interface/tickets_form.html',
                              {'formset': formset, 'flight': flight, 'fare_class': fare_class,
                               'one_ticket_price': one_ticket_price, 'comforts_prices': comforts_prices,
                               'total_booking_price': total_booking_price})

        else:
            messages.error(request, f"Form errors: {formset.errors}")
            messages.error(request, f"Non-form errors: {formset.non_form_errors()}")
        return render(request, 'passenger_interface/tickets_form.html',
                      {'formset': TicketsFormset, 'flight': flight, 'fare_class': fare_class,
                       'one_ticket_price': one_ticket_price, 'comforts_prices': comforts_prices,})
    else:
        return render(request, 'passenger_interface/tickets_form.html',
                      {'formset': TicketsFormset, 'flight': flight, 'fare_class': fare_class,
                       'one_ticket_price': one_ticket_price, 'comforts_prices': comforts_prices, })


@login_required
def profile(request):
    return render(request, 'passenger_interface/profile_profile.html')


@login_required
def profile_upcoming_bookings(request):
    upcoming_bookings = request.user.passenger_profile.bookings.filter(flight__departure_time__gt=timezone.now())
    return render(request, 'passenger_interface/profile_upcoming_bookings.html', {'bookings': upcoming_bookings, })


@login_required
def profile_previous_bookings(request):
    previous_bookings = request.user.passenger_profile.bookings.filter(flight__departure_time__lt=timezone.now())
    return render(request, 'passenger_interface/profile_previous_bookings.html', {'bookings': previous_bookings, })


@login_required
def profile_online_check_in(request):
    return render(request, 'passenger_interface/profile_online_check_in.html')


@login_required
def booking_details_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    flight = booking.flight
    return render(request, 'passenger_interface/booking_details.html',
                  {'user': request.user,
                   'tickets': booking.tickets.all(),
                   'flight': flight,
                   'email': False, }, )
