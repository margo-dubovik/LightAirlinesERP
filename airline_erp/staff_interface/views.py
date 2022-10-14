from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import TemplateView

from account.models import StaffProfile
from account.forms import StaffUserCreationForm
from airline.models import FareClass, ComfortsPrice, Airplane, Airport, Flight, Booking, Ticket, Discount
from django.utils import timezone

from .forms import TicketCodeForm, BagForm, ManagerProfileCreationForm, ManagerSearchForm, \
    AddFlightForm, StaffFlightSearchForm
from passenger_interface.views import get_baggage_price

CustomUser = get_user_model()


@login_required
@user_passes_test(lambda u: u.is_airline_staff)
def staff_profile_redirect(request):
    if request.user.staff_profile.is_gate_manager:
        return redirect(reverse('gate-manager-profile', kwargs={'id': request.user.staff_profile.pk}))
    if request.user.staff_profile.is_checkin_manager:
        return redirect(reverse('checkin-manager-profile', kwargs={'id': request.user.staff_profile.pk}))
    if request.user.staff_profile.is_supervisor:
        return redirect(reverse('supervisor-profile', kwargs={'id': request.user.staff_profile.pk}))


class GateManagerAccessMixin:

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(login_url=reverse('staff-login'), next=request.path)
        if request.user.is_airline_staff:
            if self.request.user.staff_profile.is_gate_manager or self.request.user.staff_profile.is_supervisor:
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(request, "Permission Denied!")
                return redirect(to=reverse('staff-profile-redirect'))
        else:
            messages.error(request, "Permission Denied!")
            return redirect(to=reverse('ticket-search'))


class GateManagerProfile(GateManagerAccessMixin, TemplateView):

    template_name = 'staff_interface/gate_manager_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(StaffProfile, pk=kwargs['id'])
        return context


@login_required
@user_passes_test(lambda u: u.staff_profile.is_gate_manager or u.staff_profile.is_supervisor)
def register_boarding(request):
    confirmed = request.GET.get('confirmed')
    ticket_code = request.GET.get('ticket_code')
    if confirmed:
        ticket = Ticket.objects.get(ticket_code=ticket_code)
        ticket.boarding_registered = True
        ticket.save()
        result = "Registered!"
        success = True
        return render(request, 'staff_interface/checkin_passenger.html',
                      {'result': result, 'success': success, })

    if request.method == 'POST':
        form = TicketCodeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            success = False
            try:
                ticket = Ticket.objects.get(ticket_code=cd['ticket_code'])
            except Ticket.DoesNotExist:
                ticket = None
                result = "Ticket does not exist!"
            if ticket:
                if ticket.boarding_registered:
                    result = "Ticket is already registered!"
                    return render(request, 'staff_interface/register_boarding.html',
                                  {'form': form, 'success': success, 'result': result, })
                else:
                    flight = ticket.booking.flight
                    success = True
                    return render(request, 'staff_interface/register_boarding.html',
                                  {'form': form, 'success': success,
                                   'ticket': ticket, 'flight': flight, })

            return render(request, 'staff_interface/register_boarding.html',
                          {'form': form, 'result': result, 'success': success, })
        else:
            return render(request, 'staff_interface/register_boarding.html', {'form': form, })

    else:
        form = TicketCodeForm()
        return render(request, 'staff_interface/register_boarding.html', {'form': form, })


class CheckinManagerAccessMixin:

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(login_url=reverse('staff-login'), next=request.path)
        if request.user.is_airline_staff:
            if self.request.user.staff_profile.is_checkin_manager or self.request.user.staff_profile.is_supervisor:
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(request, "Permission Denied!")
                return redirect(to=reverse('staff-profile-redirect'))
        else:
            messages.error(request, "Permission Denied!")
            return redirect(to=reverse('ticket-search'))


class CheckinManagerProfile(CheckinManagerAccessMixin, TemplateView):

    template_name = 'staff_interface/checkin_manager_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(StaffProfile, pk=kwargs['id'])
        return context


@login_required
@user_passes_test(lambda u: u.staff_profile.is_checkin_manager or u.staff_profile.is_supervisor)
def checkin_passenger(request):
    confirmed = request.GET.get('confirmed')
    ticket_code = request.GET.get('ticket_code')
    if confirmed:
        ticket = Ticket.objects.get(ticket_code=ticket_code)
        ticket.checked_in = True
        ticket.save()
        result = "Checked in!"
        success = True
        return render(request, 'staff_interface/checkin_passenger.html',
                      {'result': result, 'success': success, })

    if request.method == 'POST':
        form = TicketCodeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            success = False
            try:
                ticket = Ticket.objects.get(ticket_code=cd['ticket_code'])
            except Ticket.DoesNotExist:
                ticket = None
                result = "Ticket does not exist!"
            if ticket:
                if ticket.checked_in:
                    result = "This passenger is already checked in!"
                else:
                    flight = ticket.booking.flight
                    success = True
                    return render(request, 'staff_interface/checkin_passenger.html',
                                  {'form': form, 'success': success,
                                   'ticket': ticket, 'flight': flight, })

            return render(request, 'staff_interface/checkin_passenger.html',
                          {'form': form, 'result': result, 'success': success, })
        else:
            return render(request, 'staff_interface/checkin_passenger.html',
                          {'form': form, })

    else:
        form = TicketCodeForm()
        return render(request, 'staff_interface/checkin_passenger.html', {'form': form, })


@login_required
@user_passes_test(lambda u: u.staff_profile.is_checkin_manager or u.staff_profile.is_supervisor)
def checkin_add_options(request):
    ticket_code = request.GET.get('ticket_code')
    ticket = Ticket.objects.get(ticket_code=ticket_code)
    flight = ticket.booking.flight
    if request.method == 'POST':
        form = BagForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            additional_bags = cd['additional_bags']
            ticket.n_bags = additional_bags + ticket.n_bags
            old_baggage_price = ticket.baggage_price
            ticket.baggage_price = get_baggage_price(ticket)
            surcharge = ticket.baggage_price - old_baggage_price
            ticket.save()

            return render(request, 'staff_interface/checkin_add_options.html',
                          {'form': form, 'ticket': ticket, 'flight': flight, 'surcharge': surcharge})

        else:
            return render(request, 'staff_interface/checkin_add_options.html',
                          {'form': form, 'ticket': ticket, 'flight': flight, })

    else:
        form = BagForm()
        return render(request, 'staff_interface/checkin_add_options.html',
                      {'form': form, 'ticket': ticket, 'flight': flight})


class SupervisorAccessMixin:

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(login_url=reverse('staff-login'), next=request.path)
        if request.user.is_airline_staff:
            if self.request.user.staff_profile.is_supervisor:
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(request, "Permission Denied!")
                return redirect(to=reverse('staff-profile-redirect'))
        else:
            messages.error(request, "Permission Denied!")
            return redirect(to=reverse('ticket-search'))


class SupervisorProfile(SupervisorAccessMixin, TemplateView):

    template_name = 'staff_interface/supervisor_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(StaffProfile, pk=kwargs['id'])
        return context


class ManagersActions(SupervisorAccessMixin, TemplateView):

    template_name = 'staff_interface/managers_actions.html'


@login_required
@user_passes_test(lambda u: u.staff_profile.is_supervisor)
def managers_list(request):
    manager_type = request.GET.get('manager_type')
    managers = StaffProfile.objects.filter(role=manager_type)
    return render(request, 'staff_interface/managers_list.html',
                  {'managers': managers, 'manager_type': manager_type, })


@login_required
@user_passes_test(lambda u: u.staff_profile.is_supervisor)
def add_manager(request):
    if request.method == 'POST':
        creation_form = StaffUserCreationForm(request.POST, prefix='staff_user')
        profile_form = ManagerProfileCreationForm(request.POST, prefix='manager_profile')
        if creation_form.is_valid() and profile_form.is_valid():
            staff_user = creation_form.save()

            profile_cd = profile_form.cleaned_data
            StaffProfile.objects.create(user=staff_user, airport=profile_cd['airport'].get(),
                                        role=profile_cd['role'])

            messages.success(request, "New manager added successfully!")
            return redirect(reverse('managers-actions'))

        else:
            return render(request, 'staff_interface/supervisor_add_manager.html',
                          {'creation_form': creation_form,
                           'profile_form': profile_form,
                           })

    else:
        creation_form = StaffUserCreationForm()
        profile_form = ManagerProfileCreationForm()
        return render(request, 'staff_interface/supervisor_add_manager.html',
                      {'creation_form': creation_form,
                       'profile_form': profile_form,
                       })


@login_required
@user_passes_test(lambda u: u.staff_profile.is_supervisor)
def remove_manager(request):
    confirmed = request.GET.get('confirmed')
    manager_id = request.GET.get('manager_id')
    if confirmed:
        manager = get_object_or_404(StaffProfile, pk=manager_id)
        first_name = manager.user.first_name
        last_name = manager.user.last_name
        manager.user.delete()
        messages.info(request, f"{first_name} {last_name}'s account was deleted.")
        return redirect(reverse('remove-manager'))
    if request.method == 'POST':
        form = ManagerSearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            results = StaffProfile.objects.filter(
                Q(user__first_name__icontains=cd['manager_first_name'],
                  user__last_name__icontains=cd['manager_last_name'], )
            )
            return render(request, 'staff_interface/remove_manager.html',
                          {'form': form, 'results': results, })
        else:
            return render(request, 'staff_interface/remove_manager.html', {'form': form, })
    else:
        form = ManagerSearchForm()
        return render(request, 'staff_interface/remove_manager.html', {'form': form, })


@login_required
@user_passes_test(lambda u: u.staff_profile.is_supervisor)
def flights_actions(request):
    return render(request, 'staff_interface/flights_actions.html')


@login_required
@user_passes_test(lambda u: u.staff_profile.is_supervisor)
def add_flight(request):
    if request.method == 'POST':
        form = AddFlightForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New flight added!")
            return redirect(reverse('flights-actions'))
        else:
            return render(request, 'staff_interface/add_flight.html', {'form': form})
    else:
        form = AddFlightForm()
        return render(request, 'staff_interface/add_flight.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.staff_profile.is_supervisor)
def cancel_flight(request):
    confirmed = request.GET.get('confirmed')
    flight_id = request.GET.get('flight_id')
    if confirmed:
        flight = get_object_or_404(Flight, pk=flight_id)
        flight.is_cancelled = True
        flight.save()
        messages.info(request, f"Flight is cancelled.")
        return redirect(reverse('cancel-flight'))
    if request.method == 'POST':
        form = StaffFlightSearchForm(request.POST)
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
            print("result=", results)
            return render(request, 'staff_interface/cancel_flight.html',
                          {'form': form, 'results': results, })
        else:
            return render(request, 'staff_interface/cancel_flight.html', {'form': form, })
    else:
        form = StaffFlightSearchForm()
        return render(request, 'staff_interface/cancel_flight.html', {'form': form, })