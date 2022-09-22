from django.shortcuts import render


def home_view(request):
    return render(request, "passenger_interface/passenger_interface_home.html")

