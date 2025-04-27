from django.shortcuts import render
from .models import *

def home(request):
    adverts = Advert.objects.select_related('user', 'transport').all()
    return render(request, 'advert/home.html', {"adverts" : adverts})

def home2(request):
    return render(request, 'advert/create-advert.html', {
        'brand_list': brand_list(),
        'model_list': model_list(),
        'body_type_list': body_type_list(),
        'fuel_type_list': fuel_type_list(),
        'fuelconsumption_list': fuel_consumption_list(),
        'drive_type': drive_type(),
        'transmissiontype_list': transmission_type_list(),
        'color_list': color_list(),
        'transport_type__list': transport_type_list(),
    })

def brand_list():
    return Brand.objects.all()

def model_list():
    return Model.objects.all()

def body_type_list():
    return BodyType.objects.all()

def fuel_type_list():
    return FuelType.objects.all()

def fuel_consumption_list():
    return FuelConsumption.objects.all()

def drive_type():
    return DriveType.objects.all()

def transmission_type_list():
    return TransmissionType.objects.all()

def color_list():
    return Color.objects.all()

def transport_type_list():
    return TransmissionType.objects.all()