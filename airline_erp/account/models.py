from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.db.models.signals import post_save

from .managers import CustomUserManager

from django.conf import settings


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    is_airline_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


User = settings.AUTH_USER_MODEL


class PassengerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="passenger_profile")

    def __str__(self):
        return f"{self.user}"


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff_profile")
    airport = models.ForeignKey('airline.Airport', on_delete=models.CASCADE, related_name="staff", null=True)

    role_choices = (
        ('gate_manager', 'Gate Manager'),
        ('checkin_manager', 'Check-in manager'),
        ('supervisor', 'Supervisor'),
    )

    role = models.CharField(max_length=50, choices=role_choices)

    def __str__(self):
        return f"{self.user} staff profile"

    @property
    def is_gate_manager(self):
        return self.role == 'gate_manager'

    @property
    def is_checkin_manager(self):
        return self.role == 'checkin_manager'

    @property
    def is_supervisor(self):
        return self.role == 'supervisor'


def create_profile(sender, instance, created, **kwargs):
    if created:
        if not instance.is_airline_staff:
            PassengerProfile.objects.create(user=instance)


post_save.connect(create_profile, sender=User)
