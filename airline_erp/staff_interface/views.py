from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.conf import settings

from account.models import StaffProfile


def is_gate_manager(user):
    return user.groups.filter(name__in=['gate_managers']).exists()


def is_check_in_manager(user):
    return user.groups.filter(name__in=['check_in_managers']).exists()


def is_supervisor(user):
    return user.groups.filter(name='supervisors').exists()


@login_required
@user_passes_test(lambda u: u.is_airline_staff)
def staff_profile_redirect(request):
    if is_gate_manager(request.user):
        return redirect(reverse('gate-manager-profile'))
    print("request.user", request.user)


@login_required
@user_passes_test(is_gate_manager)
def gate_manager_profile(request):
    return render(request, 'staff_interface/gate_manager_profile')
