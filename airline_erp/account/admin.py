from django.contrib import admin
from .models import CustomUser, PassengerProfile, StaffProfile

admin.site.register(CustomUser)
admin.site.register(PassengerProfile)
admin.site.register(StaffProfile)


