from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from .models import StaffProfile

gate_managers, gate_managers_created = Group.objects.get_or_create(name='Gate Managers')
check_in_managers, check_in_managers_created = Group.objects.get_or_create(name='Check-in Managers')
supervisors, supervisors_created = Group.objects.get_or_create(name='Supervisors')
ct = ContentType.objects.get_for_model(StaffProfile)

register_passenger_boarding = Permission.objects.create(codename='can_register_boarding',
                                                        name='Can register the boarding', content_type=ct)
check_in_passenger = Permission.objects.create(codename='can_check_in_passenger', name='Can check-in passenger',
                                               content_type=ct)
add_options = Permission.objects.create(codename='can_add_convenience_options', name='Can add convenience options',
                                        content_type=ct)
take_baggage_fee = Permission.objects.create(codename='can_take_baggage_fee', name='Can take a fee for baggage',
                                             content_type=ct)
add_and_remove_managers = Permission.objects.create(codename='can_add_and_remove_managers',
                                                    name='Can add and remove the gate manager and check-in manager',
                                                    content_type=ct)
create_and_cancel_flight = Permission.objects.create(codename='can_create_or_cancel_flight',
                                                     name='Can create and cancel a flight',
                                                     content_type=ct)

gate_managers.permissions.add(register_passenger_boarding)
check_in_managers.permissions.add(check_in_passenger, add_options, take_baggage_fee)
supervisors.permissions.add(register_passenger_boarding, check_in_passenger, add_options, take_baggage_fee,
                            add_and_remove_managers, create_and_cancel_flight)
