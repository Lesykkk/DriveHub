from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.text import slugify
from django.http import Http404, JsonResponse
from .models import *
from .forms import FuelConsumptionForm, TransportForm, AdvertForm

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

@login_required
def create_advert(request):
    if request.method == 'POST':
        fuel_consumption_form = FuelConsumptionForm(request.POST)
        transport_form = TransportForm(request.POST)
        advert_form = AdvertForm(request.POST)
        if all([transport_form.is_valid(), fuel_consumption_form.is_valid(), advert_form.is_valid()]):
            fuel_consumption = fuel_consumption_form.save()

            transport = transport_form.save(commit=False)
            transport.fuel_consumption = fuel_consumption
            transport.brand_model = BrandModel.objects.get(
                brand=Brand.objects.get(value=request.POST.get("brand")),
                model=Model.objects.get(value=request.POST.get("model")),
            )
            transport.save()

            for image in request.FILES.getlist('photos'):
                TransportPhoto.objects.create(transport=transport, image=image)

            advert = advert_form.save(commit=False)
            advert.user = request.user
            advert.transport = transport
            advert.region_city = RegionCity.objects.get(
                region=Region.objects.get(value=request.POST.get("region")),
                city=City.objects.get(value=request.POST.get("city")),
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
    advert = get_object_or_404(Advert.objects.get(slug=slug))
    if advert is None:
        raise Http404()
    return render(request, 'advert/advert-detail.html', {'advert': advert})


@require_GET
def get_models_by_brand(request):
    brand_model_objects = Brand.objects.get(id=request.GET.get('brand_id')).brand_models.all()
    model_list = [{'value': bm.model.value, 'id': bm.model.id} for bm in brand_model_objects]
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

def region_list():
    return Region.objects.all()