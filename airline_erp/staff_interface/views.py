from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.conf import settings

from account.models import StaffProfile


def is_gate_manager(user):
    return user.staff_profile.role == 'gate_manager'


def is_check_in_manager(user):
    return user.staff_profile.role == 'check_in_manager'


def is_supervisor(user):
    return user.staff_profile.role == 'supervisor'


@login_required
@user_passes_test(lambda u: u.is_airline_staff)
def staff_profile_redirect(request):
    if is_gate_manager(request.user):
        return redirect(reverse('gate-manager-profile'))
    if is_check_in_manager(request.user):
        return redirect(reverse('gate-manager-profile'))
    if is_supervisor(request.user):
        return redirect(reverse('supervisor-profile'))


@login_required
@user_passes_test(is_gate_manager)
def gate_manager_profile(request):
    return render(request, 'staff_interface/gate_manager_profile.html')


@login_required
@user_passes_test(is_check_in_manager)
def checkin_manager_profile(request):
    return render(request, 'staff_interface/checkin_manager_profile.html')


@login_required
@user_passes_test(is_supervisor)
def supervisor_profile(request):
    return render(request, 'staff_interface/supervisor_profile.html')
