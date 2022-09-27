from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from .managers import CustomUserManager

from django.conf import settings


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

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

    def __str__(self):
        return f"{self.user} staff profile"
