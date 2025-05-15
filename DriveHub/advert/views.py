from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils.text import slugify
from django.http import JsonResponse, HttpResponseRedirect
from .forms import FuelConsumptionForm, TransportForm, AdvertForm
from .models import *


def home(request):
    adverts = Advert.objects.select_related('user', 'transport').all()
    adverts = list(adverts)[::-1]
    return render(request, 'advert/home.html', {
        "advert_list" : adverts,
        'brand_list': brand_list(),
        'body_type_list': body_type_list(),
        'fuel_type_list': fuel_type_list(),
        'drive_type_list': drive_type_list(),
        'transmission_type_list': transmission_type_list(),
        'region_list': region_list(),
    })

@login_required
def create_advert(request):
    if request.method == 'POST':
        fuel_consumption_form = FuelConsumptionForm(request.POST)
        transport_form = TransportForm(request.POST)
        advert_form = AdvertForm(request.POST)
        print()
        if all([transport_form.is_valid(), fuel_consumption_form.is_valid(), advert_form.is_valid()]):
            fuel_consumption = fuel_consumption_form.save()

            transport = transport_form.save(commit=False)
            transport.fuel_consumption = fuel_consumption
            transport.brand_model = BrandModel.objects.get(
                brand=Brand.objects.get(id=request.POST.get("brand")),
                model=Model.objects.get(id=request.POST.get("model")),
            )
            transport.save()

            for image in request.FILES.getlist('photos'):
                TransportPhoto.objects.create(transport=transport, image=image)

            advert = advert_form.save(commit=False)
            advert.user = request.user
            advert.transport = transport
            advert.region_city = RegionCity.objects.get(
                region=Region.objects.get(id=request.POST.get("region")),
                city=City.objects.get(id=request.POST.get("city")),
            )
            base_slug = slugify(str(transport))
            slug = base_slug
            counter = 1
            while Advert.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            advert.slug = slug
            advert.save()
            return redirect(advert.get_absolute_url())
    else:
        transport_form = TransportForm()
        fuel_consumption_form = FuelConsumptionForm()
        advert_form = AdvertForm()
    return render(request, 'advert/create-advert.html', {
        'fuel_consumption_form': fuel_consumption_form,
        'transport_form': transport_form,
        'advert_form': advert_form,

        'brand_list': brand_list(),
        'transport_type_list': transport_type_list(),
        'body_type_list': body_type_list(),
        'drive_type_list': drive_type_list(),
        'transmission_type_list': transmission_type_list(),
        'color_list': color_list(),
        'fuel_type_list': fuel_type_list(),
        'region_list': region_list(),
    })

def advert_detail(request, slug):
    advert = get_object_or_404(Advert.objects.select_related(
        'transport__fuel_consumption',
        'transport__brand_model__brand',
        'transport__brand_model__model',
        'region_city__region',
        'region_city__city',
        'user',
    ), slug=slug)

    is_favourite = False
    if request.user.is_authenticated:
        is_favourite = Favourite.objects.filter(user=request.user, advert=advert).exists()
    return render(request, 'advert/advert-detail.html', {
        'advert': advert,
        'is_favourite': is_favourite,
        'uah_price': int(advert.price * 41),
        'eur_price': int(advert.price * 0.91),
    })

@login_required
def delete_advert(request, slug):
    advert = get_object_or_404(Advert, slug=slug, user=request.user)
    if request.method == 'POST':
        advert.delete()
        # messages.success(request, 'Оголошення успішно видалене.')
        return redirect('account:my-ads')

@require_POST
@login_required
def delete_advert(request, advert_id):
    advert = get_object_or_404(Advert, id=advert_id, user=request.user)
    advert.delete()
    return JsonResponse({'redirect_url': reverse('account:my-ads')})

@require_GET
def get_models_by_brand(request):
    brand_model_objects = Brand.objects.get(id=request.GET.get('brand_id')).brand_models.all()
    model_list = [{'value': bm.model.value, 'id': bm.model.id} for bm in brand_model_objects]
    return JsonResponse(model_list, safe=False)

@require_GET
def get_cities_by_region(request):
    region_city_objects = Region.objects.get(id=request.GET.get('region_id')).region_cities.all()
    city_list = [{'value': rc.city.value, 'id': rc.city.id} for rc in region_city_objects]
    return JsonResponse(city_list, safe=False)

@require_POST
def toggle_favourite(request):
    referer = request.POST.get('referer', '/')
    
    if not request.user.is_authenticated:
        login_url = reverse('account:login')
        return JsonResponse({
            'status': 'unauthenticated',
            'login_url': f'{login_url}?next={referer}'
        })

    advert_id = request.POST.get('advert_id')
    advert = get_object_or_404(Advert, id=advert_id)
    favourite, created = Favourite.objects.get_or_create(user=request.user, advert=advert)
    
    if created:
        return JsonResponse({'status': 'added'})
    else:
        favourite.delete()
        return JsonResponse({'status': 'removed'})


def advanced_filters(request):
    filters = {
        'car_type' : request.GET.get('car_type'),
        'brand' : request.GET.get('brand'),
        'model' : request.GET.get('model'),
        'price_from' : request.GET.get('price-from'),
        'price_to' : request.GET.get('price-to'),
        'year_from' : request.GET.get('year-from'),
        'year_to' : request.GET.get('year-to'),
        'mileage_from' : request.GET.get('mileage-from'),
        'mileage_to' : request.GET.get('mileage-to'),
        'body_type' : request.GET.get('body_type'),
        'drive_type' : request.GET.get('drive_type'),
        'fuel_type' : request.GET.get('fuel_type'),
        'transmission_type' : request.GET.get('transmission_type'),
        'volume_from' : request.GET.get('volume-form'),
        'volume_to' : request.GET.get('volume-to'),
        'power_from' : request.GET.get('power-from'),
        'power_to' : request.GET.get('power-to'),
        'fuel_consumption_city_from' : request.GET.get('fuel-consumption-city-from'),
        'fuel_consumption_city_to' : request.GET.get('fuel-consumption-city-to'),
        'fuel_consumption_highway_from' : request.GET.get('fuel-consumption-highway-from'),
        'fuel_consumption_highway_to' : request.GET.get('fuel-consumption-highway-to'),
        'fuel_consumption_mixed_from' : request.GET.get('fuel-consumption-mixed-from'),
        'fuel_consumption_mixed_to' : request.GET.get('fuel-consumption-mixed-to'),
        'region' : request.GET.get('region'),
    }

    adverts = Advert.objects.select_related(
        'transport',
        'transport__transport_type',
        'transport__brand_model__brand',
        'transport__brand_model__model',
        'transport__body_type',
        'transport__fuel_type',
        'transport__fuel_consumption',
        'transport__drive_type',
        'transport__transmission_type',
        'transport__color',
        'region_city__region',
        'region_city__city',
    ).prefetch_related(
        'transport__photos',
    ).all()

    favourite_advert_ids = set()
    if request.user.is_authenticated:
        favourite_advert_ids = set(
            Favourite.objects.filter(user=request.user).values_list('advert_id', flat=True)
        )

    model_list = None

    if filters['brand']:
        adverts = adverts.filter(transport__brand_model__brand_id=filters['brand'])   
    if filters['model']:
        adverts = adverts.filter(transport__brand_model__model_id=filters['model'])
        brand_model_list = Brand.objects.get(id=filters['brand']).brand_models.select_related('model')
        model_list = [bm.model for bm in brand_model_list]
    if filters['price_from'] not in [None, '']:
        adverts = adverts.filter(price__gte=filters['price_from'])
    if filters['price_to'] not in [None, '']:
        adverts = adverts.filter(price__lte=filters['price_to'])
    if filters['year_from'] not in [None, '']:
        adverts = adverts.filter(transport__year__gte=filters['year_from'])
    if filters['year_to'] not in [None, '']:
        adverts = adverts.filter(transport__year__lte=filters['year_to'])
    if filters['mileage_from']:
        adverts = adverts.filter(transport__mileage__gte=filters['mileage_from'])
    if filters['mileage_to'] not in [None, '']:
        adverts = adverts.filter(transport__mileage__lte=filters['mileage_to'])
    if filters['body_type']:
        adverts = adverts.filter(transport__body_type_id=filters['body_type'])
    if filters['drive_type']:
        adverts = adverts.filter(transport__drive_type_id=filters['drive_type'])
    if filters['fuel_type']:
        adverts = adverts.filter(transport__fuel_type_id=filters['fuel_type'])
    if filters['transmission_type']:
        adverts = adverts.filter(transport__transmission_type_id=filters['transmission_type'])
    if filters['volume_from'] not in [None, '']:
        adverts = adverts.filter(transport__engine_volume__gte=filters['volume_from'])
    if filters['volume_to'] not in [None, '']:
        adverts = adverts.filter(transport__engine_volume__lte=filters['volume_to'])
    if filters['power_from'] not in [None, '']:
        adverts = adverts.filter(transport__engine_power__gte=filters['power_from'])
    if filters['power_to'] not in [None, '']:
        adverts = adverts.filter(transport__engine_power__lte=filters['power_to'])
    if filters['fuel_consumption_city_from'] not in [None, '']:
        adverts = adverts.filter(transport__fuel_consumption__city_consumption__gte=filters['fuel_consumption_city_from'])
    if filters['fuel_consumption_city_to'] not in [None, '']:
        adverts = adverts.filter(transport__fuel_consumption__city_consumption__lte=filters['fuel_consumption_city_to'])
    if filters['fuel_consumption_highway_from'] not in [None, '']:
        adverts = adverts.filter(transport__fuel_consumption__highway_consumption__gte=filters['fuel_consumption_highway_from'])
    if filters['fuel_consumption_highway_to'] not in [None, '']:
        adverts = adverts.filter(transport__fuel_consumption__highway_consumption__lte=filters['fuel_consumption_highway_to'])
    if filters['fuel_consumption_mixed_from'] not in [None, '']:
        adverts = adverts.filter(transport__fuel_consumption__mixed_consumption__gte=filters['fuel_consumption_mixed_from'])
    if filters['fuel_consumption_mixed_to'] not in [None, '']:
        adverts = adverts.filter(transport__fuel_consumption__mixed_consumption__lte=filters['fuel_consumption_mixed_to'])
    if filters['region']:
        adverts = adverts.filter(region_city__region_id=filters['region'])

    if filters['car_type']:
        if filters['car_type'] == 'new':
            adverts = adverts.filter(transport__mileage=0)
        elif filters['car_type'] == 'used':
            adverts = adverts.filter(transport__mileage__gt=0)

    return render(request, 'advert/advanced-filters.html',{
        'advert_list': adverts,
        'brand_list':brand_list,
        'model_list': model_list,
        'body_type_list': body_type_list(),
        'fuel_type_list': fuel_type_list(),
        'drive_type_list': drive_type_list(),
        'transmission_type_list': transmission_type_list(),
        'region_list': region_list(),
        'current_filters': filters,
        'favourite_advert_ids': favourite_advert_ids,
    })




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

def region_list():
    return Region.objects.all()