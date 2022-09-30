import pytest

from django.conf import settings
from django.contrib.auth import login
from django.urls import reverse


@pytest.mark.django_db
def test_passenger_signup(client):
    url = reverse('passenger-signup')
    resp = client.get(url)
    assert resp.status_code == 200

    form_data = {
        'email': "test@email.com",
        'first_name': "first",
        'last_name': "last",
        'password1': "testpassword1",
        'password2': "testpassword1"
    }

    resp = client.post(url, form_data)
    assert resp.status_code == 302
    assert resp.url == reverse('ticket-search')


@pytest.mark.django_db
def test_passenger_login(client, testpassenger):
    url = reverse('passenger-login')
    resp = client.get(url)
    assert resp.status_code == 200

    form_data = {
        'email': testpassenger.email,
        'password': 'strong-test-pass1!',
    }

    resp = client.post(url, form_data)
    assert resp.status_code == 302
    assert resp.url == reverse('ticket-search')


@pytest.mark.django_db
def test_passenger_login_fail(client):
    url = reverse('passenger-login')
    resp = client.get(url)
    assert resp.status_code == 200

    form_data = {
        'email': 'wrong_email@email.com',
        'password': 'wrongg-test-pass1!',
    }

    resp = client.post(url, form_data)
    messages = list(resp.context['messages'])
    assert str(messages[0]) == 'User not found'
    assert resp.status_code == 200


@pytest.mark.django_db
def test_passenger_login_as_staff(client, teststaffuser):
    url = reverse('passenger-login')
    resp = client.get(url)
    assert resp.status_code == 200

    form_data = {
        'email': teststaffuser.email,
        'password': 'strong-test-pass1!',
    }

    resp = client.post(url, form_data)
    assert resp.status_code == 302
    assert resp.url == reverse('staff-login')


@pytest.mark.django_db
def test_staff_login(client, teststaffuser):
    url = reverse('staff-login')
    resp = client.get(url)
    assert resp.status_code == 200

    form_data = {
        'email': teststaffuser.email,
        'password': 'strong-test-pass1!',
    }

    resp = client.post(url, form_data)
    assert resp.status_code == 302
    assert resp.url == reverse('staff-profile-redirect')


@pytest.mark.django_db
def test_staff_login_as_passenger(client, testpassenger):
    url = reverse('staff-login')
    resp = client.get(url)
    assert resp.status_code == 200

    form_data = {
        'email': testpassenger.email,
        'password': 'strong-test-pass1!',
    }

    resp = client.post(url, form_data)
    assert resp.status_code == 302
    assert resp.url == reverse('passenger-login')


@pytest.mark.django_db
def test_staff_login_fail(client):
    url = reverse('staff-login')
    resp = client.get(url)
    assert resp.status_code == 200

    form_data = {
        'email': 'wrong_email@email.com',
        'password': 'wrongg-test-pass1!',
    }

    resp = client.post(url, form_data)
    messages = list(resp.context['messages'])
    assert str(messages[0]) == 'User not found'
    assert resp.status_code == 200


@pytest.mark.django_db
def test_logout(client, testpassenger):
    client.force_login(testpassenger)

    url = reverse('logout')
    resp = client.get(url)
    assert resp.status_code == 302
    assert resp.url == reverse('ticket-search')

    client.force_login(testpassenger)

    url = reverse('logout')
    resp = client.get(url, follow=True)
    message = list(resp.context.get('messages'))[0]
    assert resp.status_code == 200
    assert str(message) == 'You are logged out now'






