from django.shortcuts import render
from .models import *
from django.http import JsonResponse

def home(request):
    adverts = Advert.objects.select_related('user', 'transport').all()
    return render(request, 'advert/home.html', {
        "adverts" : adverts,
        'brand_list': brand_list(),
        'brand_model_list': brand_model_list(),
        'model_list': model_list(),
        'body_type_list': body_type_list(),
        'fuel_type_list': fuel_type_list(),
        'fuelconsumption_list': fuel_consumption_list(),
        'drive_type_list': drive_type_list(),
        'transmission_type_list': transmission_type_list(),
        'color_list': color_list(),
        'transport_type_list': transport_type_list(),
    })

def create_advert(request):
    return render(request, 'advert/create-advert.html', {
        'brand_list': brand_list(),

        'brand_model_list': brand_model_list(),
        'model_list': model_list(),
        'body_type_list': body_type_list(),
        'fuel_type_list': fuel_type_list(),
        'fuelconsumption_list': fuel_consumption_list(),
        'drive_type_list': drive_type_list(),
        'transmission_type_list': transmission_type_list(),
        'color_list': color_list(),
        'transport_type_list': transport_type_list(),
    })

def get_models_by_brand(request):
    brand_model_objects = Brand.objects.get(value=request.GET.get('brand_value')).brand_models.all()
    model_list = [{
        'value': bm.model.value
    } for bm in brand_model_objects]
    return JsonResponse(model_list, safe=False)

def brand_list():
    return Brand.objects.all()

def model_list():
    return Model.objects.all()

def brand_model_list():
    return BrandModel.objects.all()

def body_type_list():
    return BodyType.objects.all()

def fuel_type_list():
    return FuelType.objects.all()

def fuel_consumption_list():
    return FuelConsumption.objects.all()

def drive_type_list():
    return DriveType.objects.all()

def transmission_type_list():
    return TransmissionType.objects.all()

def color_list():
    return Color.objects.all()

def transport_type_list():
    return TransportType.objects.all()