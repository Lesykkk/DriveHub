from django.shortcuts import render
from .models import *



def home(request):
    adverts = Advert.objects.select_related('user', 'transport').all()
    print(adverts[0].user.username)
    print(adverts[0].transport.color)
    print(adverts[0].transport.color.value)
    return render(request, 'advert/advert.html', {"adverts" : adverts})




def home2(request):
    return render(request, 'advert/create-advert.html', {
        'brand_list': brand_list(),
        'model_list': model_list(),
        'body_type_list': body_type_list(),
        'fuel_type_list': fuel_type_list(),
        'fuelconsumption_list': fuelconsumption_list(),
        'drive_wheel_type': drive_wheel_type(),
        'transmissiontype_list': transmissiontype_list(),
        'color_list': color_list(),
        'transport_type__list': transport_type_list(),
    })


def brand_list():
    return Brand.objects.all()
    
def model_list(request):
    return Model.objects.all()
    
def body_type_list(request):
    return BodyType.objects.all()

def fuel_type_list(request):
    return FuelType.objects.all()

def fuelconsumption_list(request):
    return FuelConsumption.objects.all()
    
def drive_wheel_type(request):
    return DriveWheelType.objects.all()

def transmissiontype_list(request):
    return TransmissionType.objects.all()

def color_list(request):
    return Color.objects.all()

def transport_type_list(request):
    return TransmissionType.objects.all()
