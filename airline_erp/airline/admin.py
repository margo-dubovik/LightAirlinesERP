from django.contrib import admin
from .models import FareClass, BaggagePrice, Airplane, Airport, Flight, Booking, Ticket, Discount


admin.site.register(FareClass)
admin.site.register(BaggagePrice)
admin.site.register(Airplane)
admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(Booking)
admin.site.register(Ticket)
admin.site.register(Discount)
