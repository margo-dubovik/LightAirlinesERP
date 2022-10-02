import pytest

from airline.models import FareClass, ComfortsPrice
from django.urls import reverse

from passenger_interface.views import get_fare_class_price, get_baggage_price, get_lunch_price, ticket_price_calculate


@pytest.mark.django_db
def test_get_fare_class_price(flight, discount, economy_class, business_class, first_class):
    economy_price = get_fare_class_price(flight, economy_class)
    business_price = get_fare_class_price(flight, business_class)
    first_price = get_fare_class_price(flight, first_class)
    assert economy_price == 455.00
    assert business_price == 672.00
    assert first_price == 990.00


@pytest.mark.django_db
def test_ticket_price_calculate(flight, discount, fill_comforts_price, economy_class,):
    ticket_price = ticket_price_calculate(flight, economy_class, lunch=True, n_bags=2)
    assert ticket_price == 535.00


@pytest.mark.django_db
def test_get_baggage_price(economy_class_ticket, fill_comforts_price,):
    price = get_baggage_price(economy_class_ticket)
    assert price == 70.00


@pytest.mark.django_db
def test_get_lunch_price(economy_class_ticket, fill_comforts_price,):
    price = get_lunch_price(economy_class_ticket)
    assert price == 10.00