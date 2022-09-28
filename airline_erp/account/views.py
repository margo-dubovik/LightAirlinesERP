from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import CreateView
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings

from .forms import CustomUserCreationForm, LoginForm
from .models import PassengerProfile, StaffProfile
from .token_generator import account_activation_token


CustomUser = get_user_model()


def passenger_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            next_param = request.GET.get('next')
            if next_param:
                url = next_param
            else:
                url = reverse('ticket-search')

            current_site = get_current_site(request)
            email_subject = "Welcome to LightAirlines! Please, confirm your email."
            email_body = render_to_string('account/account_activation_email.html',
                                          {'user': user,
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                           'token': account_activation_token.make_token(user),
                                           'next': url},
                                          request=request,
                                          )

            send_mail(
                subject=email_subject,
                message=" ",
                html_message=email_body,
                from_email=settings.EMAIL_FROM_USER,
                recipient_list=[user.email],
                fail_silently=True,
            )

            messages.info(request, 'We sent you an email to confirm your email address and complete the registration. '
                                   'If you do not see the email in a few minutes, check your spam folder.'
                                   'Without it you won`t be able to log in!')

            return redirect(url)
        return render(request, 'account/passenger_reg_form.html', {'form': form})

    else:
        form = CustomUserCreationForm()
        return render(request, 'account/passenger_reg_form.html', {'form': form})


def activate_passenger(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        next_param = request.GET.get('next')
        if next_param:
            url = next_param
        else:
            url = reverse('ticket-search')
        messages.success(request, 'Your email is confirmed. Thank you.')
        return redirect(url)
    else:
        return HttpResponse('Activation link is invalid!')


def passenger_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    if not user.is_staff:
                        login(request, user)
                        messages.success(request, 'Logged in successfully')
                        next_param = request.GET.get('next')
                        if next_param:
                            url = next_param
                        else:
                            url = reverse('ticket-search')
                        return redirect(url)
                    else:
                        messages.error(request, 'This account is not a passenger! Please use "Staff Log In" ')
                        return redirect(reverse('staff-login'))
                else:
                    messages.error(request, 'The account is deactivated')
            else:
                messages.error(request, 'user not found')
        return render(request, 'account/login.html', {'form': form, 'login_title': 'Log In', 'passenger': True, })
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form, 'login_title': 'Log In', 'passenger': True, })


def staff_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_airline_staff:
                    login(request, user)
                    messages.success(request, 'Logged in successfully')
                    return redirect(reverse('staff-profile-redirect'))
                else:
                    messages.error(request, 'This account is not a staff member! Please use "Log In"')
                    return redirect(reverse('passenger-login'))
            else:
                messages.error(request, 'user not found')
        return render(request, 'account/login.html', {'form': form, 'login_title': 'Staff Log In', })
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form, 'login_title': 'Staff Log In', })


def user_logout(request):
    logout(request)
    messages.info(request, 'You are logged out now')
    return redirect(reverse('ticket-search'))
