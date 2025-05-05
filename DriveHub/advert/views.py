from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import (
    Brand, Model, BrandModel, BodyType, FuelType, FuelConsumption, DriveType,
    TransmissionType, Color, TransportType, Transport, TransportPhoto, Advert
)

def home(request):
    adverts = Advert.objects.select_related('user', 'transport').all()
    return render(request, 'advert/home.html', {"adverts": adverts})


@login_required
def create_advert(request):
    if request.method == 'POST':
        try:
            
            required_fields = [
                'brand', 'model', 'transport_type', 'year', 'body_type', 'fuel_type',
                'engine_volume', 'engine_power', 'fuel_city', 'fuel_highway', 'fuel_mixed',
                'drive_type', 'transmission_type', 'color', 'mileage', 'owners_number',
                'price', 'city', 'description'
            ]
            missing = [field for field in required_fields if not request.POST.get(field)]
            if missing:
                messages.error(request, f"Відсутні обов'язкові поля : {', '.join(missing)}")
                raise ValueError("Обов'язкові поля не заповнені")

            
            images = request.FILES.getlist('image')
            if len(images) < 6:
                messages.error(request, "Потрібно додати щонайменше 6 фотографій.")
                raise ValueError("Недостатньо фтогафій")

            # brand & model
            brand = Brand.objects.get(value=request.POST['brand'])
            model = Model.objects.get(value=request.POST['model'])
            brand_model, _ = BrandModel.objects.get_or_create(brand=brand, model=model)

            
            fuel_consumption = FuelConsumption.objects.create(
                city=request.POST['fuel_city'],
                highway=request.POST['fuel_highway'],
                mixed=request.POST['fuel_mixed']
            )

            # pereviritu
            transport = Transport.objects.create(
                transport_type=TransportType.objects.get(id=request.POST['transport_type']),
                brand_model=brand_model,
                year=int(request.POST['year']),
                body_type=BodyType.objects.get(id=request.POST['body_type']),
                fuel_type=FuelType.objects.get(id=request.POST['fuel_type']),
                engine_volume=float(request.POST['engine_volume']),
                engine_power=int(request.POST['engine_power']),
                fuel_consumption=fuel_consumption,
                drive_type=DriveType.objects.get(id=request.POST['drive_type']),
                transmission_type=TransmissionType.objects.get(id=request.POST['transmission_type']),
                color=Color.objects.get(id=request.POST['color']),
                mileage=int(request.POST['mileage']),
                owners_number=int(request.POST['owners_number'])
            )

            
            advert = Advert.objects.create(
                user=request.user,
                transport=transport,
                slug=slugify(f"{brand.value}-{model.value}-{transport.year}-{request.user.id}"),
                price=int(request.POST['price']),
                city=request.POST['city'],
                description=request.POST['description']
            )

          
            for image in images:
                TransportPhoto.objects.create(transport=transport, image=image)

            messages.success(request, "Оголошення  створено! ")
            return redirect('advert:home')

        except Exception as e:
            # Якщо помилка не додалася вище через messages, додамо тут
            if not messages.get_messages(request):
                messages.error(request, f"Сталася помилка: {str(e)}")
            # повертаємо форму з повідомленнями
            return render(request, 'advert/create-advert.html', {
                'brand_list': brand_list(),
                'brand_model_list': brand_model_list(),
                'model_list': model_list(),
                'body_type_list': body_type_list(),
                'fuel_type_list': fuel_type_list(),
                'fuelconsumption_list': fuel_consumption_list(),
                'drive_type_list': drive_type(),
                'transmission_type_list': transmission_type_list(),
                'color_list': color_list(),
                'transport_type_list': transport_type_list(),
            })

    
    return render(request, 'advert/create-advert.html', {
        'brand_list': brand_list(),
        'brand_model_list': brand_model_list(),
        'model_list': model_list(),
        'body_type_list': body_type_list(),
        'fuel_type_list': fuel_type_list(),
        'fuelconsumption_list': fuel_consumption_list(),
        'drive_type_list': drive_type(),
        'transmission_type_list': transmission_type_list(),
        'color_list': color_list(),
        'transport_type_list': transport_type_list(),
    })


def get_models_by_brand(request):
    brand_model_objects = Brand.objects.get(value=request.GET.get('brand_value')).brand_models.all()
    model_list = [{'value': bm.model.value} for bm in brand_model_objects]
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

def drive_type():
    return DriveType.objects.all()

def transmission_type_list():
    return TransmissionType.objects.all()

def color_list():
    return Color.objects.all()

def transport_type_list():
    return TransportType.objects.all()
