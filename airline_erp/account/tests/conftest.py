import pytest


@pytest.fixture
def testpassenger(db, django_user_model):
    email = 'test_passenger@test.com'
    password = 'strong-test-pass1!'
    first_name = 'test_first_name'
    last_name = 'test_last_name'
    passenger = django_user_model.objects.create_user(email=email, password=password, first_name=first_name,
                                                      last_name=last_name, is_airline_staff=False)
    passenger.is_active = True
    return passenger


@pytest.fixture
def teststaffuser(db, django_user_model):
    email = 'test_staff_member@test.com'
    password = 'strong-test-pass1!'
    first_name = 'staff_first_name'
    last_name = 'staff_last_name'
    staffuser = django_user_model.objects.create_user(email=email, password=password, first_name=first_name,
                                                      last_name=last_name, is_airline_staff=True)
    return staffuser
